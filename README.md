# Ticketing System - GUI

A lightweight desktop ticket management application built with **Python** and **CustomTkinter**.

The application provides a simple graphical interface for creating, viewing, editing, searching, and deleting tickets, as well as adding notes to existing tickets.

Ticket data is stored locally in a JSON file, so no external database or server is required.

---
## ⚠️ IMPORTANT NOTES

**IMPORTANT: This application is a LIGHTWEIGHT LOCAL TICKET MANAGER and is NOT designed to operate as a MULTI-USER, NETWORK-BASED, or SERVER-BASED TICKETING PLATFORM.**

The application is intended for **LOCAL, SINGLE-USER USE**. It does not provide the **SECURITY, ACCESS CONTROL, SYNCHRONIZATION, CONCURRENCY HANDLING,** or **INFRASTRUCTURE** normally required for a **MULTI-USER** or **PRODUCTION SERVER ENVIRONMENT**.

**DO NOT DEPLOY OR USE THIS APPLICATION AS A SHARED SERVER-BASED TICKETING SYSTEM** unless you have independently implemented and verified the required **SECURITY, AUTHENTICATION, AUTHORIZATION, SYNCHRONIZATION, BACKUP,** and **DATA-PROTECTION MECHANISMS**.

The current application does **NOT** provide:

- **AUTHENTICATION**
- **USER ACCOUNTS**
- **ROLE-BASED PERMISSIONS OR ACCESS CONTROL**
- **NETWORK SYNCHRONIZATION**
- **MULTI-USER CONCURRENCY CONTROL**
- **DATABASE-BACKED STORAGE**
- **CLOUD SYNCHRONIZATION**
- **AUTOMATIC BACKUPS**
- **AUDIT LOGGING**
- **ENCRYPTION OF STORED TICKET DATA**
- **SERVER-SIDE ACCESS CONTROL**
- **PROTECTION AGAINST SIMULTANEOUS MODIFICATION OF THE JSON DATA FILE**
- **BUILT-IN RECOVERY MECHANISMS FOR DATA LOSS OR CORRUPTION**

Ticket data is stored locally in a JSON file named `tickets_gui.json`.

**THE JSON FILE IS NOT ENCRYPTED BY THE APPLICATION** and may contain **TICKET INFORMATION, NOTES, USER NAMES,** or other potentially **SENSITIVE DATA**. You are solely responsible for **PROTECTING THE FILE** and **RESTRICTING ACCESS TO IT**.

**DO NOT STORE SENSITIVE, CONFIDENTIAL, REGULATED, OR SECURITY-CRITICAL INFORMATION IN THE APPLICATION** unless you have independently implemented appropriate **PROTECTION MECHANISMS**.

Using the application in an environment for which it was not designed is entirely at the user's **OWN RISK AND RESPONSIBILITY**, to the maximum extent permitted by applicable law.

---
## Screenshot

## Screenshot

![Ticketing System GUI](assets/screenshot.png)

---

---

## Features

* Create new tickets
* Edit existing tickets
* Delete tickets
* Search tickets in real time
* Add notes to tickets
* Assign tickets to users
* Set ticket priority
* Set ticket status
* Add tags to tickets
* View ticket creation and update timestamps
* Local JSON-based data storage
* Dark graphical interface
* No external database required

---

## Ticket Information

Each ticket can contain the following information:

| Field       | Description                        |
| ----------- | ---------------------------------- |
| ID          | Unique numeric identifier          |
| Title       | Short title of the ticket          |
| Description | Detailed description of the issue  |
| Reporter    | Person who reported the ticket     |
| Assignee    | Person assigned to the ticket      |
| Priority    | `Low`, `Medium`, or `High`         |
| Status      | `Open`, `In Progress`, or `Closed` |
| Tags        | Comma-separated tags               |
| Notes       | Additional notes with timestamps   |
| Created At  | Ticket creation time in UTC        |
| Updated At  | Last update time in UTC            |

---

## Requirements

* Python 3.9 or newer
* `customtkinter`

The application also uses Python standard-library modules, including:

* `json`
* `os`
* `dataclasses`
* `datetime`
* `typing`
* `tkinter`

---

## Installation

Clone or download the project:

```bash
git clone <repository-url>
cd <project-directory>
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```powershell
.\venv\Scripts\Activate.ps1
```

If you are using Command Prompt instead of PowerShell:

```cmd
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

After activating the virtual environment, install the required dependency:

```bash
python -m pip install customtkinter
```

It is recommended to install dependencies only after activating the virtual environment so they remain isolated from your system-wide Python installation.

---

## Running the Application

Make sure the virtual environment is activated.

Then run:

```bash
python ticketing-v3.py
```

After starting, the graphical interface will open automatically.

To verify that the virtual environment is active, your terminal should normally show `(venv)` at the beginning of the command prompt.

When you are finished using the application, you can leave the virtual environment with:

```bash
deactivate
```

---

## Data Storage

Ticket data is stored in:

```text
tickets_gui.json
```

The file is created automatically in the application's working directory when tickets are saved.

Example structure:

```json
[
    {
        "id": 1,
        "title": "Login button not responding",
        "description": "The login button does not respond when the user enters valid credentials.",
        "reporter": "Ali",
        "priority": "High",
        "status": "Open",
        "assignee": "Unassigned",
        "tags": [
            "bug",
            "authentication",
            "ui"
        ],
        "notes": [
            "[2026-08-19T17:16:29.243731+00:00] Issue reproduced and confirmed."
        ],
        "created_at": "2026-08-19T17:10:41.803087+00:00",
        "updated_at": "2026-08-19T17:16:29.243731+00:00"
    },
    {
        "id": 2,
        "title": "Update dashboard layout",
        "description": "Improve the dashboard layout and make the navigation easier to use.",
        "reporter": "Sara",
        "priority": "Medium",
        "status": "In Progress",
        "assignee": "Reza",
        "tags": [
            "ui",
            "dashboard",
            "improvement"
        ],
        "notes": [
            "[2026-08-19T17:15:44.903745+00:00] Initial layout reviewed.",
            "[2026-08-19T17:15:54.831331+00:00] Navigation changes are currently being implemented."
        ],
        "created_at": "2026-08-19T17:15:34.955220+00:00",
        "updated_at": "2026-08-19T17:15:54.831376+00:00"
    },
    {
        "id": 3,
        "title": "Add CSV export",
        "description": "Allow users to export ticket information to a CSV file.",
        "reporter": "Mina",
        "priority": "Low",
        "status": "Closed",
        "assignee": "Ali",
        "tags": [
            "feature",
            "export",
            "csv"
        ],
        "notes": [
            "[2026-08-20T08:30:00+00:00] CSV export implemented.",
            "[2026-08-20T09:10:00+00:00] Export functionality tested successfully."
        ],
        "created_at": "2026-08-20T08:00:00+00:00",
        "updated_at": "2026-08-20T09:10:00+00:00"
    }
]
```

The application does not require a separate database server.

---

## Search

The search field can find tickets using:

* Ticket ID
* Title
* Description
* Reporter
* Assignee
* Priority
* Status
* Tags
* Notes

Search is performed as the user types.

---

## Ticket Status

The application currently supports:

```text
Open
In Progress
Closed
```

---

## Ticket Priority

The available priority levels are:

```text
Low
Medium
High
```

---

## Notes

Notes can be added to an existing ticket.

Each note is automatically stored together with a UTC timestamp.

Example:

```text
[2026-08-20T10:20:30+00:00] Investigated the reported issue.
```

---

## Time Handling

Ticket timestamps are generated using UTC and stored in ISO 8601 format.

This helps keep stored timestamps consistent across different systems and time zones.

---

## Project Structure

A basic project layout may look like this:

```text
project/
├── ticketing-v3.py
├── tickets_gui.json
├── README.md
├── LICENSE
└── venv/
```

`tickets_gui.json` is generated automatically after tickets are saved.

The `venv/` directory contains the project's Python virtual environment and is normally not committed to version control.

---

## Architecture

The application is divided into three main parts.

### Data Model

The `Ticket` dataclass represents individual tickets and handles conversion between Python objects and JSON-compatible dictionaries.

### Ticket Management

The `TicketSystem` class handles:

* Loading tickets
* Saving tickets
* Creating tickets
* Finding tickets
* Updating tickets
* Deleting tickets
* Adding notes
* Searching tickets

### Graphical Interface

The `TicketingApp` class provides the desktop GUI using CustomTkinter.

It handles:

* Ticket list display
* Search
* Ticket details
* Ticket creation
* Ticket editing
* Notes
* Ticket deletion

---

## Error Handling

The application attempts to handle common local-storage problems.

If the JSON data file does not exist, an empty ticket list is used.

If the JSON file is invalid or cannot be read, the application starts with an empty ticket list instead of terminating immediately.

Save failures are reported as runtime errors.

---

## Backup

Because ticket data is stored in a local JSON file, creating backups is straightforward.

Simply copy:

```text
tickets_gui.json
```

to a safe location.

For important data, regular backups are recommended.

---

## Limitations

The current implementation is intentionally simple.

Some possible future improvements include:

* SQLite database support
* Automatic backups
* Ticket filtering
* Sorting
* Pagination
* User authentication
* Role-based access control
* Attachments
* Export to CSV or JSON
* Import from existing ticket data
* Ticket history and audit logs
* Notifications
* Multi-user support
* Server/API support
* Improved validation
* Packaging as a standalone Windows application

---

## License

This project is distributed under the **project-specific Software License Terms** included with the project.

See:

```text
LICENSE
```

for the complete terms governing use, modification, redistribution, warranty, and limitation of liability.

The Software is provided **"AS IS"**, without warranty of any kind, to the maximum extent permitted by applicable law.

Users are responsible for determining whether their use, deployment, modification, or distribution of the Software is appropriate, lawful, safe, and suitable for their intended environment.

---

## Author

**Parsa Esmaili**

Copyright © 2026 Parsa Esmaili.
