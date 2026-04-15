# 📚 Library Management System
> **Layered Architecture Demo** — Python 3 + SQLite

---

## Thành viên nhóm

| Thành viên | Phụ trách |
|---|---|
| Thành viên 1 | Database Layer + Persistence Layer (DAO) |
| Thành viên 2 | Business Layer (Service) |
| Thành viên 3 | Presentation Layer + GitHub + README |

---

## Kiến trúc hệ thống

Dự án áp dụng **Layered Architecture (Kiến trúc phân tầng)** gồm 4 tầng:

```
┌──────────────────────────────────────────┐
│  Layer 1 — Presentation                  │
│  BookView  │  MemberView  │  BorrowView  │
│  (Console UI, nhận input từ người dùng)  │
└──────────────────┬───────────────────────┘
                   │ gọi xuống
┌──────────────────▼───────────────────────┐
│  Layer 2 — Business Logic                │
│  BookService │ MemberService │ BorrowService │
│  (Validate, enforce rules, orchestrate)  │
└──────────────────┬───────────────────────┘
                   │ gọi xuống
┌──────────────────▼───────────────────────┐
│  Layer 3 — Persistence (DAO)             │
│  BookDAO  │  MemberDAO  │  BorrowDAO     │
│  (CRUD thuần túy với DB)                 │
└──────────────────┬───────────────────────┘
                   │ gọi xuống
┌──────────────────▼───────────────────────┐
│  Layer 4 — Database                      │
│  DBConnection  (SQLite connection pool)  │
└──────────────────────────────────────────┘
```

**Quy tắc quan trọng:** Mỗi tầng chỉ được gọi xuống tầng ngay bên dưới — không bỏ qua tầng.

---

## Cấu trúc thư mục

```
LibraryApp/
├── main.py                         ← Entry point
├── Database/
│   └── DBConnection.py             ← Layer 4: Quản lý kết nối SQLite
├── Persistence/
│   ├── BookDAO.py                  ← Layer 3: CRUD sách
│   ├── MemberDAO.py                ← Layer 3: CRUD thành viên
│   └── BorrowDAO.py                ← Layer 3: CRUD phiếu mượn
├── Business/
│   ├── BookService.py              ← Layer 2: Logic nghiệp vụ sách
│   ├── MemberService.py            ← Layer 2: Logic nghiệp vụ thành viên
│   └── BorrowService.py            ← Layer 2: Logic mượn/trả sách
└── Presentation/
    ├── BookView.py                 ← Layer 1: UI quản lý sách
    ├── MemberView.py               ← Layer 1: UI quản lý thành viên
    └── BorrowView.py               ← Layer 1: UI mượn/trả sách
```

---

## Database — 3 bảng

```sql
-- Bảng 1: Sách
CREATE TABLE Books (
    BookId    INTEGER PRIMARY KEY AUTOINCREMENT,
    Title     TEXT    NOT NULL,
    Author    TEXT    NOT NULL,
    Quantity  INTEGER NOT NULL DEFAULT 0
);

-- Bảng 2: Thành viên
CREATE TABLE Members (
    MemberId  INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName  TEXT    NOT NULL,
    Email     TEXT    NOT NULL UNIQUE
);

-- Bảng 3: Phiếu mượn
CREATE TABLE BorrowRecords (
    RecordId   INTEGER PRIMARY KEY AUTOINCREMENT,
    BookId     INTEGER NOT NULL,
    MemberId   INTEGER NOT NULL,
    BorrowDate TEXT    NOT NULL,
    ReturnDate TEXT,                          -- NULL = chưa trả
    FOREIGN KEY (BookId)   REFERENCES Books(BookId),
    FOREIGN KEY (MemberId) REFERENCES Members(MemberId)
);
```

File DB (`library.db`) được tạo tự động khi chạy lần đầu.

---

## Business Rules (Layer 2)

| Rule | Mô tả |
|---|---|
| Validate input | Title/Author/FullName không được rỗng |
| Email format | Kiểm tra định dạng email bằng regex |
| Email unique | Không cho đăng ký email trùng |
| Quantity check | Không mượn sách khi `Quantity = 0` |
| Auto-decrement | Mượn sách → `Quantity - 1` tự động |
| Auto-increment | Trả sách → `Quantity + 1` tự động |
| Date validation | `ReturnDate >= BorrowDate` |
| Double return | Không cho trả sách đã được trả rồi |
| Overdue detection | Phát hiện phiếu mượn quá 14 ngày |

---

## Cách chạy

### Yêu cầu
- Python 3.8 trở lên (không cần cài thêm thư viện — dùng SQLite có sẵn)

### Chạy ứng dụng

```bash
# Clone repo
git clone <your-repo-url>
cd LibraryApp

# Chạy
python main.py
```

### Menu chính

```
========================================
    LIBRARY MANAGEMENT SYSTEM
    Layered Architecture Demo
========================================
1. Book Management
2. Member Management
3. Borrow / Return
0. Exit
```

---

## Phân công chi tiết

### Thành viên 1 — Database + Persistence Layer

**Files:** `Database/DBConnection.py`, `Persistence/BookDAO.py`, `Persistence/MemberDAO.py`, `Persistence/BorrowDAO.py`

Công việc:
- Viết script SQL tạo 3 bảng
- Implement `DBConnection` với `get_connection()` và `initialize_database()`
- Implement toàn bộ phương thức CRUD cho 3 DAO
- Đảm bảo `PRAGMA foreign_keys = ON` để enforce FK constraint

### Thành viên 2 — Business Layer

**Files:** `Business/BookService.py`, `Business/MemberService.py`, `Business/BorrowService.py`

Công việc:
- Validate input (rỗng, định dạng, số âm, ...)
- Enforce business rules (kiểm tra số lượng, kiểm tra ngày, ...)
- Orchestrate giữa các DAO khi cần (BorrowService dùng cả BookService và MemberService)
- Trả về dict `{"success": bool, ...}` thống nhất cho Presentation Layer

### Thành viên 3 — Presentation + GitHub + README

**Files:** `Presentation/BookView.py`, `Presentation/MemberView.py`, `Presentation/BorrowView.py`, `main.py`, `README.md`

Công việc:
- Viết console UI cho cả 3 nghiệp vụ
- Setup GitHub repo, cấu trúc thư mục
- Viết README
- Merge code và test tổng thể

---

## Demo chạy thử

```
[DB] Database initialized successfully.

========================================
    LIBRARY MANAGEMENT SYSTEM
========================================
Choose: 1

===== BOOK MANAGEMENT =====
Choose: 3
  Title  : Clean Code
  Author : Robert C. Martin
  Qty    : 5
[OK] Book added with ID = 1

Choose: 3  (Borrow/Return)
  Book ID   : 1
  Member ID : 1
  Borrow date: (blank = today)
[OK] Borrow record created. Record ID = 1
```
