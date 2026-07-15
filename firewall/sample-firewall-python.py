import json
import random
import time
from dataclasses import dataclass, field
from collections import Counter


# =========================
# Data Models
# =========================

@dataclass
class Packet:
    timestamp: float
    src_ip: str
    dst_port: int
    protocol: str


@dataclass
class IPState:
    score: float = 0.0
    hits: int = 0
    blocked_until: float = 0.0
    last_seen: float = 0.0
    level: str = "OK"


@dataclass
class FirewallConfig:
    # Allowed list / scoring policy
    allowed_ports: set = field(default_factory=lambda: {22, 80, 443})

    weight_non_allowed_port: float = 2.0
    weight_rare_port: float = 1.0

    # Multi-stage thresholds
    warn_score_threshold: float = 4.0
    warn_min_hits: int = 2

    block_score_threshold_short: float = 7.0
    block_duration_seconds_short: float = 3.0
    short_min_hits: int = 3

    block_score_threshold_long: float = 10.0
    block_duration_seconds_long: float = 10.0
    long_min_hits: int = 4

    quarantine_score_threshold: float = 14.0
    quarantine_min_hits: int = 5
    quarantine_duration_seconds: float = 30.0

    # Score decay
    decay_rate: float = 0.08  # score decreases per second


# =========================
# Engine
# =========================

class FirewallEngine:
    def __init__(self, config: FirewallConfig):
        self.config = config
        self.states: dict[str, IPState] = {}

    def get_state(self, src_ip: str) -> IPState:
        if src_ip not in self.states:
            self.states[src_ip] = IPState()
        return self.states[src_ip]

    def decay_score(self, state: IPState, current_time: float) -> None:
        # If first time, just initialize last_seen
        if state.last_seen == 0.0:
            state.last_seen = current_time
            return

        dt = max(0.0, current_time - state.last_seen)
        state.score = max(0.0, state.score - self.config.decay_rate * dt)
        state.last_seen = current_time

    def process(self, packet: Packet) -> str:
        state = self.get_state(packet.src_ip)
        self.decay_score(state, packet.timestamp)

        # If currently blocked
        if packet.timestamp < state.blocked_until:
            return "BLOCKED"

        # Score update policy
        score_add = 0.0

        if packet.dst_port not in self.config.allowed_ports:
            score_add += self.config.weight_non_allowed_port

        # "rare" ports heuristic (outside common set)
        if packet.dst_port not in {22, 80, 443}:
            score_add += self.config.weight_rare_port

        state.score += score_add
        state.hits += 1

        # Escalation decision
        if (state.score >= self.config.quarantine_score_threshold
                and state.hits >= self.config.quarantine_min_hits):
            state.blocked_until = packet.timestamp + self.config.quarantine_duration_seconds
            state.level = "QUARANTINE"
            return "QUARANTINE"

        if (state.score >= self.config.block_score_threshold_long
                and state.hits >= self.config.long_min_hits):
            state.blocked_until = packet.timestamp + self.config.block_duration_seconds_long
            state.level = "BLOCK_LONG"
            return "BLOCK_LONG"

        if (state.score >= self.config.block_score_threshold_short
                and state.hits >= self.config.short_min_hits):
            state.blocked_until = packet.timestamp + self.config.block_duration_seconds_short
            state.level = "BLOCK_SHORT"
            return "BLOCK_SHORT"

        if (state.score >= self.config.warn_score_threshold
                and state.hits >= self.config.warn_min_hits):
            state.level = "WARN"
            return "WARN"

        state.level = "OK"
        return "ACCEPT"


# =========================
# Logger
# =========================

class JSONLLogger:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def write(self, event: dict) -> None:
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")


# =========================
# Source (Traffic Simulation)
# =========================

def generate_packets(num_packets=2000, ip_pool=100, seed=42):
    random.seed(seed)
    packets = []

    base = time.time()
    ips = [f"192.168.1.{i}" for i in range(1, ip_pool + 1)]

    # mix allowed + suspicious ports
    allowed = [22, 80, 443]
    suspicious = [8080, 3306, 5000, 6379, 21, 23, 25, 53, 1099]
    ports = allowed + suspicious

    protocols = ["TCP", "UDP"]

    for _ in range(num_packets):
        src_ip = random.choice(ips)
        dst_port = random.choice(ports)
        protocol = random.choice(protocols)
        timestamp = base + random.random() * 12.0
        packets.append(Packet(timestamp, src_ip, dst_port, protocol))

    packets.sort(key=lambda p: p.timestamp)
    return packets


# =========================
# App
# =========================

class FirewallApp:
    def __init__(self, engine: FirewallEngine, packets: list[Packet], logger: JSONLLogger):
        self.engine = engine
        self.packets = packets
        self.logger = logger
        self.actions_counter = Counter()

        self.important_actions = {"WARN", "BLOCK_SHORT", "BLOCK_LONG", "QUARANTINE", "BLOCKED"}

    def run(self):
        start_time = time.time()
        total_packets = 0

        for packet in self.packets:
            action = self.engine.process(packet)
            total_packets += 1
            self.actions_counter[action] += 1

            state = self.engine.get_state(packet.src_ip)
            event = {
                "timestamp": packet.timestamp,
                "src_ip": packet.src_ip,
                "dst_port": packet.dst_port,
                "protocol": packet.protocol,
                "action": action,
                "score": state.score,
                "hits": state.hits,
                "blocked_until": state.blocked_until,
                "level": state.level,
            }

            self.logger.write(event)

            if action in self.important_actions:
                print(
                    f"{action} {self._emoji(action)} | "
                    f"t={packet.timestamp:.2f} ip={packet.src_ip} "
                    f"port={packet.dst_port} score={state.score:.1f} hits={state.hits} "
                    f"until={state.blocked_until:.2f}"
                )

        end_time = time.time()
        self._print_summary(total_packets=total_packets, end_time=end_time, start_time=start_time)

    def _emoji(self, action: str) -> str:
        return {
            "ACCEPT": "✅",
            "WARN": "⚠️",
            "BLOCK_SHORT": "⏱️",
            "BLOCK_LONG": "🚫",
            "QUARANTINE": "🧯",
            "BLOCKED": "🧱",
        }.get(action, "🔸")

    def _print_summary(self, total_packets: int, end_time: float, start_time: float):
        print("\n=== خلاصه شبیه‌سازی ===")
        print(f"مدت زمان: {end_time - start_time:.2f} ثانیه")
        print(f"تعداد بسته‌ها: {total_packets}")
        print(f"آی‌پی‌های مورد بررسی: {len(self.engine.states)}\n")

        order = ["ACCEPT", "WARN", "BLOCK_SHORT", "BLOCK_LONG", "QUARANTINE", "BLOCKED"]
        for act in order:
            cnt = self.actions_counter.get(act, 0)
            if cnt > 0:
                print(f"{self._emoji(act)} {act}: {cnt}")


# =========================
# Main
# =========================

if __name__ == "__main__":
    config = FirewallConfig()
    engine = FirewallEngine(config)

    packets = generate_packets(num_packets=200, ip_pool=1033, seed=42)

    logger = JSONLLogger("firewall_events.jsonl")
    app = FirewallApp(engine=engine, packets=packets, logger=logger)
    app.run()
