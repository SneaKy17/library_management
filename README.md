# Library Management App

A custom Frappe/ERPNext application for managing a library — members, books, and transactions.

## Features

- **Library Member** — Register and manage library members with membership type (Standard / Premium / VIP) and status
- **Book** — Catalog books with title, author, ISBN, category, and copy availability tracking
- **Book Transaction** — Record book issue and return transactions, track due dates and status

## DocTypes

| DocType | Naming Series | Description |
|---------|--------------|-------------|
| Library Member | `LIB-MEM-#####` | Stores member details and membership info |
| Book | `BOOK-#####` | Stores book catalog with availability |
| Book Transaction | `TXN-#####` | Records issue/return transactions |

## Tech Stack

- **Framework**: Frappe v16 / ERPNext v16
- **Database**: MariaDB
- **Deployment**: Docker (frappe_docker)

## Setup Instructions

### Prerequisites
- Docker Desktop installed and running
- frappe_docker cloned from https://github.com/frappe/frappe_docker

### Quick Start

```bash
# Start containers
docker-compose -f pwd.yml up -d

# Install app on site
docker exec frappe_docker-backend-1 bench --site frontend install-app library_management

# Run migrations
docker exec frappe_docker-backend-1 bench --site frontend migrate

# Clear cache
docker exec frappe_docker-backend-1 bench --site frontend clear-cache
```

### Access

Open http://localhost:8080 and login with `Administrator` / `admin`

| Module | URL |
|--------|-----|
| Library Member | http://localhost:8080/app/library-member |
| Book | http://localhost:8080/app/book |
| Book Transaction | http://localhost:8080/app/book-transaction |

## Project Structure

```
library_management/
├── library_management/
│   ├── __init__.py
│   ├── hooks.py              # App configuration & hooks
│   ├── modules.txt           # Module declarations
│   └── doctype/
│       ├── library_member/
│       │   ├── library_member.json   # DocType schema
│       │   └── library_member.py    # Controller
│       ├── book/
│       │   ├── book.json
│       │   └── book.py
│       └── book_transaction/
│           ├── book_transaction.json
│           └── book_transaction.py
├── setup.py
├── requirements.txt
└── README.md
```

## License

MIT
