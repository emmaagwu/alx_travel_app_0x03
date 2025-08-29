# CRM Project

This is a **Django-based CRM (Customer Relationship Management) application** that includes background task processing with **Celery + RabbitMQ**, and scheduled jobs with **django-crontab**.

---

## 🚀 Features

- Customer Management (CRUD)
- Low-stock check and notifications
- Automated CRM report generation
- Scheduled background tasks with **Celery**
- Cron-based jobs with **django-crontab**
- Logging of reports and tasks to `/tmp/crm_report_log.txt`

---

## 🛠️ Tech Stack

- **Backend**: Django (Python 3.10+)
- **Task Queue**: Celery
- **Message Broker**: RabbitMQ
- **Scheduling**: django-crontab
- **Database**: SQLite (default, can be switched to PostgreSQL/MySQL)

---

## 📦 Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-username/crm.git
cd crm
