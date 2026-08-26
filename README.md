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

* **AUTHENTICATION**
* **USER ACCOUNTS**
* **ROLE-BASED PERMISSIONS OR ACCESS CONTROL**
* **NETWORK SYNCHRONIZATION**
* **MULTI-USER CONCURRENCY CONTROL**
* **DATABASE-BACKED STORAGE**
* **CLOUD SYNCHRONIZATION**
* **AUTOMATIC BACKUPS**
* **AUDIT LOGGING**
* **ENCRYPTION OF STORED TICKET DATA**
* **SERVER-SIDE ACCESS CONTROL**
* **PROTECTION AGAINST SIMULTANEOUS MODIFICATION OF THE JSON DATA FILE**
* **BUILT-IN RECOVERY MECHANISMS FOR DATA LOSS OR CORRUPTION**

Ticket data is stored locally in a JSON file named `tickets_gui.json`.

**THE JSON FILE IS NOT ENCRYPTED BY THE APPLICATION** and may contain **TICKET INFORMATION, NOTES, USER NAMES,** or other potentially **SENSITIVE DATA**. You are solely responsible for **PROTECTING THE FILE** and **RESTRICTING ACCESS TO IT**.

**DO NOT STORE SENSITIVE, CONFIDENTIAL, REGULATED, OR SECURITY-CRITICAL INFORMATION IN THE APPLICATION** unless you have independently implemented appropriate **PROTECTION MECHANISMS**.

Using the application in an environment for which it was not designed is entirely at the user's **OWN RISK AND RESPONSIBILITY**, to the maximum extent permitted by applicable law.

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

---

# ترجمه‌ی فارسی

<div dir="rtl" align="right">

# سامانه‌ی مدیریت تیکت — رابط گرافیکی

یک برنامه‌ی دسکتاپ سبک برای مدیریت تیکت است که با **Python** و **CustomTkinter** ساخته شده است.

این برنامه یک رابط گرافیکی ساده برای ایجاد، مشاهده، ویرایش، جستجو و حذف تیکت‌ها و همچنین افزودن یادداشت به تیکت‌های موجود ارائه می‌دهد.

اطلاعات تیکت‌ها به‌صورت محلی در یک فایل JSON ذخیره می‌شوند؛ بنابراین برنامه به پایگاه داده یا سرور خارجی نیاز ندارد.

---

## ⚠️ نکات مهم

**مهم: این برنامه یک مدیریت‌کننده‌ی سبک و محلی تیکت است و برای استفاده به‌عنوان یک سامانه‌ی تیکتینگ چندکاربره، شبکه‌ای یا مبتنی بر سرور طراحی نشده است.**

این برنامه برای **استفاده‌ی محلی و تک‌کاربره** در نظر گرفته شده است. برنامه امکانات **امنیت، کنترل دسترسی، همگام‌سازی، مدیریت هم‌زمانی** یا **زیرساخت** مورد نیاز برای یک محیط **چندکاربره یا سرور Production** را فراهم نمی‌کند.

**این برنامه را به‌عنوان یک سامانه‌ی تیکتینگ اشتراکی و مبتنی بر سرور Deploy یا استفاده نکنید**؛ مگر اینکه خودتان سازوکارهای لازم برای **امنیت، احراز هویت، مجوزدهی، همگام‌سازی، پشتیبان‌گیری و حفاظت از داده‌ها** را به‌صورت مستقل پیاده‌سازی و بررسی کرده باشید.

نسخه‌ی فعلی برنامه امکانات زیر را **فراهم نمی‌کند**:

* **احراز هویت (Authentication)**
* **حساب‌های کاربری**
* **مجوزهای مبتنی بر نقش یا کنترل دسترسی**
* **همگام‌سازی شبکه‌ای**
* **کنترل هم‌زمانی برای چند کاربر**
* **ذخیره‌سازی مبتنی بر پایگاه داده**
* **همگام‌سازی ابری**
* **پشتیبان‌گیری خودکار**
* **ثبت رویدادهای حسابرسی (Audit Logging)**
* **رمزنگاری اطلاعات ذخیره‌شده‌ی تیکت‌ها**
* **کنترل دسترسی سمت سرور**
* **محافظت در برابر تغییر هم‌زمان فایل JSON**
* **سازوکار داخلی بازیابی در صورت از دست رفتن یا خراب شدن داده‌ها**

اطلاعات تیکت‌ها به‌صورت محلی در فایلی با نام `tickets_gui.json` ذخیره می‌شوند.

**فایل JSON توسط برنامه رمزنگاری نمی‌شود** و ممکن است شامل **اطلاعات تیکت، یادداشت‌ها، نام کاربران** یا سایر داده‌های بالقوه **حساس** باشد. مسئولیت کامل **محافظت از فایل و محدود کردن دسترسی به آن** بر عهده‌ی شماست.

**اطلاعات حساس، محرمانه، تحت مقررات یا حیاتی از نظر امنیتی را در این برنامه ذخیره نکنید**؛ مگر اینکه خودتان سازوکارهای مناسب **حفاظت از داده‌ها** را پیاده‌سازی کرده باشید.

استفاده از برنامه در محیطی که برای آن طراحی نشده است، تا حداکثر میزان مجاز طبق قوانین قابل اجرا، کاملاً بر عهده و مسئولیت **خود کاربر** است.

---

## امکانات

* ایجاد تیکت‌های جدید
* ویرایش تیکت‌های موجود
* حذف تیکت‌ها
* جستجوی لحظه‌ای تیکت‌ها
* افزودن یادداشت به تیکت‌ها
* اختصاص دادن تیکت‌ها به کاربران
* تعیین اولویت تیکت
* تعیین وضعیت تیکت
* افزودن برچسب به تیکت‌ها
* مشاهده‌ی زمان ایجاد و آخرین به‌روزرسانی تیکت
* ذخیره‌سازی محلی مبتنی بر JSON
* رابط گرافیکی با حالت تیره
* عدم نیاز به پایگاه داده‌ی خارجی

---

## اطلاعات تیکت

هر تیکت می‌تواند شامل اطلاعات زیر باشد:

| فیلد        | توضیحات                                  |
| ----------- | ---------------------------------------- |
| ID          | شناسه‌ی عددی یکتا                        |
| Title       | عنوان کوتاه تیکت                         |
| Description | توضیحات کامل مشکل                        |
| Reporter    | شخصی که تیکت را گزارش کرده است           |
| Assignee    | شخص اختصاص‌یافته به تیکت                 |
| Priority    | اولویت: `Low`، `Medium` یا `High`        |
| Status      | وضعیت: `Open`، `In Progress` یا `Closed` |
| Tags        | برچسب‌های جداشده با کاما                 |
| Notes       | یادداشت‌های اضافی همراه با زمان ثبت      |
| Created At  | زمان ایجاد تیکت بر اساس UTC              |
| Updated At  | زمان آخرین به‌روزرسانی بر اساس UTC       |

---

## پیش‌نیازها

* Python نسخه‌ی 3.9 یا جدیدتر
* `customtkinter`

برنامه همچنین از ماژول‌های استاندارد Python زیر استفاده می‌کند:

* `json`
* `os`
* `dataclasses`
* `datetime`
* `typing`
* `tkinter`

---

## نصب

ابتدا پروژه را Clone یا Download کنید:

```bash
git clone <repository-url>
cd <project-directory>
```

یک محیط مجازی Python ایجاد کنید:

```bash
python -m venv venv
```

سپس محیط مجازی را فعال کنید.

### Windows

```powershell
.\venv\Scripts\Activate.ps1
```

اگر به‌جای PowerShell از Command Prompt استفاده می‌کنید:

```cmd
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

پس از فعال کردن محیط مجازی، وابستگی مورد نیاز را نصب کنید:

```bash
python -m pip install customtkinter
```

توصیه می‌شود وابستگی‌ها را پس از فعال کردن محیط مجازی نصب کنید تا از نصب Python سراسری سیستم جدا باقی بمانند.

---

## اجرای برنامه

مطمئن شوید محیط مجازی فعال است.

سپس اجرا کنید:

```bash
python ticketing-v3.py
```

پس از اجرا، رابط گرافیکی برنامه به‌صورت خودکار باز خواهد شد.

برای اطمینان از فعال بودن محیط مجازی، معمولاً عبارت `(venv)` در ابتدای خط فرمان ترمینال نمایش داده می‌شود.

پس از پایان کار با برنامه، می‌توانید از محیط مجازی خارج شوید:

```bash
deactivate
```

---

## ذخیره‌سازی داده‌ها

اطلاعات تیکت‌ها در فایل زیر ذخیره می‌شوند:

```text
tickets_gui.json
```

این فایل هنگام ذخیره شدن تیکت‌ها، به‌صورت خودکار در پوشه‌ی کاری برنامه ایجاد می‌شود.

ساختار نمونه:

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
    }
]
```

برنامه به یک سرور پایگاه داده‌ی جداگانه نیاز ندارد.

---

## جستجو

فیلد جستجو می‌تواند تیکت‌ها را بر اساس موارد زیر پیدا کند:

* شناسه‌ی تیکت
* عنوان
* توضیحات
* گزارش‌دهنده
* مسئول تیکت
* اولویت
* وضعیت
* برچسب‌ها
* یادداشت‌ها

جستجو هم‌زمان با تایپ کردن کاربر انجام می‌شود.

---

## وضعیت تیکت

برنامه در حال حاضر از وضعیت‌های زیر پشتیبانی می‌کند:

```text
Open
In Progress
Closed
```

---

## اولویت تیکت

سطوح اولویت موجود عبارت‌اند از:

```text
Low
Medium
High
```

---

## یادداشت‌ها

می‌توان به تیکت‌های موجود یادداشت اضافه کرد.

هر یادداشت به‌صورت خودکار همراه با یک Timestamp بر اساس UTC ذخیره می‌شود.

نمونه:

```text
[2026-08-20T10:20:30+00:00] Investigated the reported issue.
```

---

## مدیریت زمان

Timestampهای مربوط به تیکت‌ها با استفاده از UTC تولید و با فرمت ISO 8601 ذخیره می‌شوند.

این کار باعث می‌شود Timestampهای ذخیره‌شده در سیستم‌ها و منطقه‌های زمانی مختلف، سازگاری بیشتری داشته باشند.

---

## ساختار پروژه

ساختار پایه‌ی پروژه می‌تواند به شکل زیر باشد:

```text
project/
├── ticketing-v3.py
├── tickets_gui.json
├── README.md
├── LICENSE
└── venv/
```

فایل `tickets_gui.json` پس از ذخیره شدن تیکت‌ها به‌صورت خودکار ایجاد می‌شود.

پوشه‌ی `venv/` محیط مجازی Python پروژه را در خود نگه می‌دارد و معمولاً نباید در Version Control Commit شود.

---

## معماری

برنامه به سه بخش اصلی تقسیم شده است.

### مدل داده (Data Model)

`dataclass` مربوط به `Ticket` تیکت‌های جداگانه را نمایش می‌دهد و تبدیل بین اشیای Python و دیکشنری‌های سازگار با JSON را مدیریت می‌کند.

### مدیریت تیکت (Ticket Management)

کلاس `TicketSystem` وظایف زیر را مدیریت می‌کند:

* بارگذاری تیکت‌ها
* ذخیره‌ی تیکت‌ها
* ایجاد تیکت
* پیدا کردن تیکت‌ها
* به‌روزرسانی تیکت‌ها
* حذف تیکت‌ها
* افزودن یادداشت
* جستجوی تیکت‌ها

### رابط گرافیکی (Graphical Interface)

کلاس `TicketingApp` رابط گرافیکی دسکتاپ را با استفاده از CustomTkinter فراهم می‌کند.

این کلاس موارد زیر را مدیریت می‌کند:

* نمایش فهرست تیکت‌ها
* جستجو
* جزئیات تیکت
* ایجاد تیکت
* ویرایش تیکت
* یادداشت‌ها
* حذف تیکت

---

## مدیریت خطا

برنامه تلاش می‌کند مشکلات رایج مربوط به ذخیره‌سازی محلی را مدیریت کند.

اگر فایل JSON مربوط به داده‌ها وجود نداشته باشد، از یک فهرست خالی تیکت استفاده می‌شود.

اگر فایل JSON نامعتبر باشد یا قابل خواندن نباشد، برنامه با یک فهرست خالی از تیکت‌ها شروع به کار می‌کند و بلافاصله متوقف نمی‌شود.

خطاهای مربوط به ذخیره‌سازی به‌صورت `RuntimeError` گزارش می‌شوند.

---

## پشتیبان‌گیری

از آنجا که اطلاعات تیکت‌ها در یک فایل JSON محلی ذخیره می‌شوند، تهیه‌ی نسخه‌ی پشتیبان ساده است.

کافی است فایل زیر را:

```text
tickets_gui.json
```

در یک مکان امن کپی کنید.

برای داده‌های مهم، تهیه‌ی نسخه‌ی پشتیبان به‌صورت منظم توصیه می‌شود.

---

## محدودیت‌ها

پیاده‌سازی فعلی عمداً ساده نگه داشته شده است.

برخی قابلیت‌هایی که می‌توان در آینده اضافه کرد:

* پشتیبانی از پایگاه داده‌ی SQLite
* پشتیبان‌گیری خودکار
* فیلتر کردن تیکت‌ها
* مرتب‌سازی
* صفحه‌بندی (Pagination)
* احراز هویت کاربران
* کنترل دسترسی مبتنی بر نقش
* پیوست‌ها
* خروجی CSV یا JSON
* وارد کردن داده‌های تیکت موجود
* تاریخچه‌ی تیکت و Audit Log
* اعلان‌ها
* پشتیبانی از چند کاربر
* پشتیبانی از Server/API
* اعتبارسنجی بهتر داده‌ها
* بسته‌بندی به‌عنوان یک برنامه‌ی مستقل برای Windows

---

## مجوز (License)

این پروژه تحت **Project-specific Software License Terms** موجود در پروژه توزیع می‌شود.

برای مشاهده‌ی شرایط کامل مربوط به استفاده، تغییر، بازتوزیع، ضمانت و محدودیت مسئولیت، فایل زیر را ببینید:

```text
LICENSE
```

این نرم‌افزار **«AS IS»**، یعنی «به همان شکل موجود»، و بدون هیچ‌گونه ضمانتی ارائه می‌شود؛ تا حداکثر میزان مجاز طبق قوانین قابل اجرا.

کاربران مسئول تعیین این موضوع هستند که استفاده، Deployment، تغییر یا توزیع نرم‌افزار برای محیط مورد نظرشان مناسب، قانونی، ایمن و قابل استفاده است یا خیر.

---

## نویسنده

**پارسا اسمعیلی**

Copyright © 2026 Parsa Esmaili.

</div>
