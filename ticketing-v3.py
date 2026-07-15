import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

import customtkinter as ctk
from tkinter import messagebox, simpledialog


# ============================================================
# تنظیمات کلی ظاهر برنامه
# ============================================================
ctk.set_appearance_mode("dark")      # حالت تیره
ctk.set_default_color_theme("blue")   # تم پیش‌فرض آبی


# ============================================================
# ابزارهای کمکی
# ============================================================

def now_iso() -> str:
    """
    زمان فعلی را به صورت ISO8601 و با timezone UTC برمی‌گرداند.
    """
    return datetime.now(timezone.utc).isoformat()


def parse_tags(tags_text: str) -> List[str]:
    """
    متن برچسب‌ها را که با کاما جدا شده‌اند، به لیست تبدیل می‌کند.
    مثال:
        "bug, ui, urgent" -> ["bug", "ui", "urgent"]
    """
    return [tag.strip() for tag in tags_text.split(",") if tag.strip()]


def tags_to_text(tags: List[str]) -> str:
    """
    لیست برچسب‌ها را به متن قابل نمایش تبدیل می‌کند.
    """
    return ", ".join(tags) if tags else "-"


# ============================================================
# مدل داده
# ============================================================

@dataclass
class Ticket:
    """
    نماینده‌ی یک تیکت.
    """
    id: int
    title: str
    description: str
    reporter: str
    priority: str = "Medium"
    status: str = "Open"
    assignee: str = "Unassigned"
    tags: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        """
        تبدیل شیء Ticket به دیکشنری برای ذخیره در JSON.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "reporter": self.reporter,
            "priority": self.priority,
            "status": self.status,
            "assignee": self.assignee,
            "tags": self.tags,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Ticket":
        """
        ساخت Ticket از داده‌ی دیکشنری.
        """
        return cls(
            id=int(data.get("id", 0)),
            title=data.get("title", ""),
            description=data.get("description", ""),
            reporter=data.get("reporter", ""),
            priority=data.get("priority", "Medium"),
            status=data.get("status", "Open"),
            assignee=data.get("assignee", "Unassigned"),
            tags=data.get("tags", []) or [],
            notes=data.get("notes", []) or [],
            created_at=data.get("created_at", now_iso()),
            updated_at=data.get("updated_at", now_iso()),
        )


# ============================================================
# منطق مدیریت تیکت‌ها
# ============================================================

class TicketSystem:
    """
    مدیریت ذخیره، بارگذاری و عملیات مربوط به تیکت‌ها.
    """

    def __init__(self, filename: str = "tickets_gui.json"):
        self.filename = filename
        self.tickets: List[Ticket] = self._load()

    def _load(self) -> List[Ticket]:
        """
        تیکت‌ها را از فایل JSON بارگذاری می‌کند.
        اگر فایل وجود نداشته باشد یا خراب باشد، لیست خالی برمی‌گرداند.
        """
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                return []

            return [Ticket.from_dict(item) for item in data]

        except (json.JSONDecodeError, OSError):
            # اگر فایل خراب باشد یا باز نشود، برنامه نمی‌ترکد؛ فقط خونسرد می‌ماند.
            return []

    def _save(self) -> None:
        """
        تیکت‌ها را در فایل JSON ذخیره می‌کند.
        """
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(
                    [ticket.to_dict() for ticket in self.tickets],
                    f,
                    ensure_ascii=False,
                    indent=4,
                )
        except OSError as e:
            raise RuntimeError(f"Failed to save tickets: {e}")

    def _next_id(self) -> int:
        """
        شناسه‌ی بعدی را تولید می‌کند.
        """
        if not self.tickets:
            return 1
        return max(ticket.id for ticket in self.tickets) + 1

    def add_ticket(
        self,
        title: str,
        description: str,
        reporter: str,
        priority: str = "Medium",
        assignee: str = "Unassigned",
        tags: Optional[List[str]] = None,
    ) -> Ticket:
        """
        تیکت جدید می‌سازد و ذخیره می‌کند.
        """
        ticket = Ticket(
            id=self._next_id(),
            title=title,
            description=description,
            reporter=reporter,
            priority=priority,
            assignee=assignee,
            tags=tags or [],
        )
        self.tickets.append(ticket)
        self._save()
        return ticket

    def get_ticket(self, ticket_id: int) -> Optional[Ticket]:
        """
        تیکت را با شناسه پیدا می‌کند.
        """
        for ticket in self.tickets:
            if ticket.id == ticket_id:
                return ticket
        return None

    def delete_ticket(self, ticket_id: int) -> bool:
        """
        تیکت را حذف می‌کند.
        """
        before = len(self.tickets)
        self.tickets = [t for t in self.tickets if t.id != ticket_id]
        if len(self.tickets) != before:
            self._save()
            return True
        return False

    def update_ticket(
        self,
        ticket_id: int,
        title: str,
        description: str,
        reporter: str,
        priority: str,
        status: str,
        assignee: str,
        tags: List[str],
    ) -> bool:
        """
        اطلاعات یک تیکت را ویرایش می‌کند.
        """
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return False

        ticket.title = title
        ticket.description = description
        ticket.reporter = reporter
        ticket.priority = priority
        ticket.status = status
        ticket.assignee = assignee
        ticket.tags = tags
        ticket.updated_at = now_iso()

        self._save()
        return True

    def add_note(self, ticket_id: int, note: str) -> bool:
        """
        یک یادداشت جدید به تیکت اضافه می‌کند.
        """
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return False

        ticket.notes.append(f"[{now_iso()}] {note}")
        ticket.updated_at = now_iso()
        self._save()
        return True

    def search_tickets(self, query: str) -> List[Ticket]:
        """
        در عنوان، توضیحات، گزارش‌دهنده، برچسب‌ها و assignee جستجو می‌کند.
        """
        query = query.strip().lower()
        if not query:
            return self.tickets[:]

        results = []
        for ticket in self.tickets:
            haystack = " ".join([
                str(ticket.id),
                ticket.title,
                ticket.description,
                ticket.reporter,
                ticket.priority,
                ticket.status,
                ticket.assignee,
                " ".join(ticket.tags),
                " ".join(ticket.notes),
            ]).lower()

            if query in haystack:
                results.append(ticket)

        return results


# ============================================================
# رابط کاربری گرافیکی
# ============================================================

class TicketingApp(ctk.CTk):
    """
    برنامه‌ی اصلی GUI.
    """

    def __init__(self):
        super().__init__()

        # منطق داده
        self.system = TicketSystem()
        self.selected_ticket_id: Optional[int] = None

        # تنظیمات پنجره اصلی
        self.title("Ticketing System - GUI")
        self.geometry("1200x720")
        self.minsize(1000, 650)

        # چیدمان کلی
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ساخت بخش‌ها
        self._build_sidebar()
        self._build_main_area()
        self._build_details_panel()

        # بارگذاری اولیه
        self.refresh_ticket_list()

    # --------------------------------------------------------
    # ساخت UI
    # --------------------------------------------------------

    def _build_sidebar(self):
        """
        پنل سمت چپ: جستجو + لیست تیکت‌ها + دکمه‌های اصلی
        """
        self.sidebar = ctk.CTkFrame(self, corner_radius=14)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        self.sidebar.grid_rowconfigure(2, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self.sidebar,
            text="🎫 Ticket Manager",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")

        self.search_entry = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="Search tickets...",
        )
        self.search_entry.grid(row=1, column=0, padx=16, pady=8, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self._on_search)

        # فریم اسکرول‌دار برای لیست تیکت‌ها
        self.ticket_scroll = ctk.CTkScrollableFrame(self.sidebar, corner_radius=12)
        self.ticket_scroll.grid(row=2, column=0, padx=16, pady=8, sticky="nsew")

        # دکمه‌های پایین
        self.btn_new = ctk.CTkButton(
            self.sidebar,
            text="+ New Ticket",
            command=self.open_new_ticket_window,
        )
        self.btn_new.grid(row=3, column=0, padx=16, pady=(8, 6), sticky="ew")

        self.btn_refresh = ctk.CTkButton(
            self.sidebar,
            text="Refresh",
            fg_color="#4b5563",
            hover_color="#374151",
            command=self.refresh_ticket_list,
        )
        self.btn_refresh.grid(row=4, column=0, padx=16, pady=6, sticky="ew")

    def _build_main_area(self):
        """
        پنل میانی/اصلی: اطلاعات خلاصه‌ی تیکت انتخاب‌شده
        """
        self.main_area = ctk.CTkFrame(self, corner_radius=14)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=(0, 12), pady=12)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(1, weight=1)

        header = ctk.CTkLabel(
            self.main_area,
            text="Ticket Details",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        header.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")

        self.details_frame = ctk.CTkFrame(self.main_area, corner_radius=12)
        self.details_frame.grid(row=1, column=0, padx=16, pady=8, sticky="nsew")
        self.details_frame.grid_columnconfigure(0, weight=1)

        self.details_text = ctk.CTkTextbox(self.details_frame, wrap="word")
        self.details_text.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")
        self.details_text.configure(state="disabled")

        self.actions_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.actions_frame.grid(row=2, column=0, padx=16, pady=(8, 16), sticky="ew")
        self.actions_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_edit = ctk.CTkButton(
            self.actions_frame,
            text="Edit",
            command=self.open_edit_ticket_window,
        )
        self.btn_edit.grid(row=0, column=0, padx=6, sticky="ew")

        self.btn_note = ctk.CTkButton(
            self.actions_frame,
            text="Add Note",
            fg_color="#0f766e",
            hover_color="#115e59",
            command=self.add_note_dialog,
        )
        self.btn_note.grid(row=0, column=1, padx=6, sticky="ew")

        self.btn_delete = ctk.CTkButton(
            self.actions_frame,
            text="Delete",
            fg_color="#b91c1c",
            hover_color="#7f1d1d",
            command=self.delete_selected_ticket,
        )
        self.btn_delete.grid(row=0, column=2, padx=6, sticky="ew")

    def _build_details_panel(self):
        """
        در این نسخه، همان main_area نقش پنل جزئیات را هم دارد.
        این متد برای خوانایی نگه داشته شده.
        """
        pass

    # --------------------------------------------------------
    # منطق نمایش
    # --------------------------------------------------------

    def refresh_ticket_list(self, tickets: Optional[List[Ticket]] = None):
        """
        لیست تیکت‌ها را بازسازی می‌کند.
        """
        for widget in self.ticket_scroll.winfo_children():
            widget.destroy()

        ticket_list = tickets if tickets is not None else self.system.tickets

        if not ticket_list:
            empty = ctk.CTkLabel(
                self.ticket_scroll,
                text="No tickets yet.",
                text_color="gray",
            )
            empty.pack(pady=20)
            self.show_details(None)
            return

        for ticket in sorted(ticket_list, key=lambda t: t.id):
            self._add_ticket_item(ticket)

        # اگر قبلاً تیکتی انتخاب شده بود، سعی کن دوباره نمایش بده
        if self.selected_ticket_id:
            ticket = self.system.get_ticket(self.selected_ticket_id)
            self.show_details(ticket)
        else:
            self.show_details(None)

    def _add_ticket_item(self, ticket: Ticket):
        """
        یک آیتم قابل کلیک برای هر تیکت در sidebar می‌سازد.
        """
        frame = ctk.CTkFrame(self.ticket_scroll, corner_radius=10)
        frame.pack(fill="x", padx=4, pady=4)

        color = {
            "High": "#dc2626",
            "Medium": "#d97706",
            "Low": "#16a34a",
        }.get(ticket.priority, "#2563eb")

        title = ctk.CTkLabel(
            frame,
            text=f"#{ticket.id} | {ticket.title}",
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        title.pack(fill="x", padx=10, pady=(8, 2))

        meta = ctk.CTkLabel(
            frame,
            text=f"{ticket.status} • {ticket.priority} • {ticket.reporter}",
            text_color=color,
            anchor="w",
        )
        meta.pack(fill="x", padx=10, pady=(0, 8))

        # با کلیک روی فریم یا متن، جزئیات نمایش داده شود
        frame.bind("<Button-1>", lambda e, t=ticket: self.show_details(t))
        title.bind("<Button-1>", lambda e, t=ticket: self.show_details(t))
        meta.bind("<Button-1>", lambda e, t=ticket: self.show_details(t))

    def show_details(self, ticket: Optional[Ticket]):
        """
        جزئیات تیکت را در پنل اصلی نشان می‌دهد.
        """
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", "end")

        if ticket is None:
            self.details_text.insert("end", "Select a ticket to see details.")
            self.selected_ticket_id = None
        else:
            self.selected_ticket_id = ticket.id
            details = f"""ID: {ticket.id}
Title: {ticket.title}
Description: {ticket.description}

Reporter: {ticket.reporter}
Assignee: {ticket.assignee}
Priority: {ticket.priority}
Status: {ticket.status}
Tags: {tags_to_text(ticket.tags)}

Created At: {ticket.created_at}
Updated At: {ticket.updated_at}

Notes:
"""
            self.details_text.insert("end", details)

            if ticket.notes:
                for i, note in enumerate(ticket.notes, start=1):
                    self.details_text.insert("end", f"{i}. {note}\n")
            else:
                self.details_text.insert("end", "- No notes yet.\n")

        self.details_text.configure(state="disabled")

    # --------------------------------------------------------
    # رویداد جستجو
    # --------------------------------------------------------

    def _on_search(self, event=None):
        """
        هنگام تایپ در جستجو، لیست را فیلتر می‌کند.
        """
        query = self.search_entry.get()
        results = self.system.search_tickets(query)
        self.refresh_ticket_list(results)

    # --------------------------------------------------------
    # پنجره ساخت تیکت جدید
    # --------------------------------------------------------

    def open_new_ticket_window(self):
        """
        پنجره‌ی ساخت تیکت جدید را باز می‌کند.
        """
        window = ctk.CTkToplevel(self)
        window.title("New Ticket")
        window.geometry("520x620")
        window.grab_set()

        window.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(window, text="Create New Ticket", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.grid(row=0, column=0, padx=16, pady=(16, 10), sticky="w")

        entry_title = ctk.CTkEntry(window, placeholder_text="Title")
        entry_title.grid(row=1, column=0, padx=16, pady=8, sticky="ew")

        entry_desc = ctk.CTkTextbox(window, height=120)
        entry_desc.grid(row=2, column=0, padx=16, pady=8, sticky="ew")
        entry_desc.insert("1.0", "Description...")

        entry_reporter = ctk.CTkEntry(window, placeholder_text="Reporter")
        entry_reporter.grid(row=3, column=0, padx=16, pady=8, sticky="ew")

        entry_assignee = ctk.CTkEntry(window, placeholder_text="Assignee (optional)")
        entry_assignee.grid(row=4, column=0, padx=16, pady=8, sticky="ew")

        combo_priority = ctk.CTkComboBox(window, values=["Low", "Medium", "High"])
        combo_priority.grid(row=5, column=0, padx=16, pady=8, sticky="ew")
        combo_priority.set("Medium")

        combo_status = ctk.CTkComboBox(window, values=["Open", "In Progress", "Closed"])
        combo_status.grid(row=6, column=0, padx=16, pady=8, sticky="ew")
        combo_status.set("Open")

        entry_tags = ctk.CTkEntry(window, placeholder_text="Tags (comma separated)")
        entry_tags.grid(row=7, column=0, padx=16, pady=8, sticky="ew")

        def save_new_ticket():
            title = entry_title.get().strip()
            description = entry_desc.get("1.0", "end").strip()
            reporter = entry_reporter.get().strip()
            assignee = entry_assignee.get().strip() or "Unassigned"
            priority = combo_priority.get().strip()
            status = combo_status.get().strip()
            tags = parse_tags(entry_tags.get())

            if not title or not description or not reporter:
                messagebox.showwarning("Missing Data", "Title, Description and Reporter are required.")
                return

            self.system.add_ticket(
                title=title,
                description=description,
                reporter=reporter,
                priority=priority,
                assignee=assignee,
                tags=tags,
            )

            # اگر خواستی، وضعیت اولیه را بعد از ساخت تنظیم می‌کنیم
            new_ticket = self.system.tickets[-1]
            new_ticket.status = status
            new_ticket.updated_at = now_iso()
            self.system._save()

            self.refresh_ticket_list()
            window.destroy()
            messagebox.showinfo("Success", "Ticket created successfully.")

        btn_save = ctk.CTkButton(window, text="Save Ticket", command=save_new_ticket)
        btn_save.grid(row=8, column=0, padx=16, pady=(16, 8), sticky="ew")

    # --------------------------------------------------------
    # پنجره ویرایش تیکت
    # --------------------------------------------------------

    def open_edit_ticket_window(self):
        """
        پنجره ویرایش تیکت انتخاب‌شده را باز می‌کند.
        """
        ticket = self.system.get_ticket(self.selected_ticket_id) if self.selected_ticket_id else None
        if not ticket:
            messagebox.showwarning("No Selection", "Please select a ticket first.")
            return

        window = ctk.CTkToplevel(self)
        window.title(f"Edit Ticket #{ticket.id}")
        window.geometry("520x660")
        window.grab_set()

        window.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(window, text=f"Edit Ticket #{ticket.id}", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, padx=16, pady=(16, 10), sticky="w"
        )

        entry_title = ctk.CTkEntry(window)
        entry_title.insert(0, ticket.title)
        entry_title.grid(row=1, column=0, padx=16, pady=8, sticky="ew")

        entry_desc = ctk.CTkTextbox(window, height=120)
        entry_desc.grid(row=2, column=0, padx=16, pady=8, sticky="ew")
        entry_desc.insert("1.0", ticket.description)

        entry_reporter = ctk.CTkEntry(window)
        entry_reporter.insert(0, ticket.reporter)
        entry_reporter.grid(row=3, column=0, padx=16, pady=8, sticky="ew")

        entry_assignee = ctk.CTkEntry(window)
        entry_assignee.insert(0, ticket.assignee)
        entry_assignee.grid(row=4, column=0, padx=16, pady=8, sticky="ew")

        combo_priority = ctk.CTkComboBox(window, values=["Low", "Medium", "High"])
        combo_priority.set(ticket.priority)
        combo_priority.grid(row=5, column=0, padx=16, pady=8, sticky="ew")

        combo_status = ctk.CTkComboBox(window, values=["Open", "In Progress", "Closed"])
        combo_status.set(ticket.status)
        combo_status.grid(row=6, column=0, padx=16, pady=8, sticky="ew")

        entry_tags = ctk.CTkEntry(window)
        entry_tags.insert(0, tags_to_text(ticket.tags))
        entry_tags.grid(row=7, column=0, padx=16, pady=8, sticky="ew")

        def save_changes():
            title = entry_title.get().strip()
            description = entry_desc.get("1.0", "end").strip()
            reporter = entry_reporter.get().strip()
            assignee = entry_assignee.get().strip() or "Unassigned"
            priority = combo_priority.get().strip()
            status = combo_status.get().strip()
            tags = parse_tags(entry_tags.get())

            if not title or not description or not reporter:
                messagebox.showwarning("Missing Data", "Title, Description and Reporter are required.")
                return

            ok = self.system.update_ticket(
                ticket_id=ticket.id,
                title=title,
                description=description,
                reporter=reporter,
                priority=priority,
                status=status,
                assignee=assignee,
                tags=tags,
            )

            if ok:
                self.refresh_ticket_list()
                window.destroy()
                messagebox.showinfo("Success", "Ticket updated successfully.")
            else:
                messagebox.showerror("Error", "Failed to update ticket.")

        btn_save = ctk.CTkButton(window, text="Save Changes", command=save_changes)
        btn_save.grid(row=8, column=0, padx=16, pady=(16, 8), sticky="ew")

    # --------------------------------------------------------
    # افزودن یادداشت
    # --------------------------------------------------------

    def add_note_dialog(self):
        """
        یک پنجره ساده برای اضافه کردن یادداشت باز می‌کند.
        """
        if not self.selected_ticket_id:
            messagebox.showwarning("No Selection", "Please select a ticket first.")
            return

        note = simpledialog.askstring("Add Note", "Enter note:")
        if not note or not note.strip():
            return

        ok = self.system.add_note(self.selected_ticket_id, note.strip())
        if ok:
            self.refresh_ticket_list()
            ticket = self.system.get_ticket(self.selected_ticket_id)
            self.show_details(ticket)
            messagebox.showinfo("Success", "Note added successfully.")
        else:
            messagebox.showerror("Error", "Failed to add note.")

    # --------------------------------------------------------
    # حذف تیکت
    # --------------------------------------------------------

    def delete_selected_ticket(self):
        """
        تیکت انتخاب‌شده را حذف می‌کند.
        """
        if not self.selected_ticket_id:
            messagebox.showwarning("No Selection", "Please select a ticket first.")
            return

        ticket = self.system.get_ticket(self.selected_ticket_id)
        if not ticket:
            messagebox.showerror("Error", "Selected ticket not found.")
            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete ticket #{ticket.id}?\n\nTitle: {ticket.title}"
        )

        if answer:
            ok = self.system.delete_ticket(ticket.id)
            if ok:
                self.selected_ticket_id = None
                self.refresh_ticket_list()
                messagebox.showinfo("Deleted", "Ticket deleted successfully.")
            else:
                messagebox.showerror("Error", "Failed to delete ticket.")


# ============================================================
# اجرای برنامه
# ============================================================

if __name__ == "__main__":
    app = TicketingApp()
    app.mainloop()

