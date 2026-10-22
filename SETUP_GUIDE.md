# Quick Setup Guide - IG Portal

## 🚀 Quick Start (Automated)

Run the setup script:

```bash
cd igportal
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Run database migrations
- Optionally load initial data
- Optionally create a superuser
- Collect static files

## 📋 Manual Setup Steps

### 1. Create Virtual Environment

```bash
cd igportal
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**If mysqlclient installation fails on macOS:**
```bash
brew install mysql-client
export PATH="/usr/local/opt/mysql-client/bin:$PATH"
pip install mysqlclient
```

### 3. Setup MySQL Database

```bash
# Start MySQL (if not running)
# macOS: brew services start mysql
# Linux: sudo systemctl start mysql

# Create database
mysql -u root -p
```

In MySQL prompt:
```sql
CREATE DATABASE ig2026 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 4. Configure Database Settings

Edit `igportal/settings.py` and update:
- Database password
- Database port (if not using default 3306)

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Load Initial Data (Optional)

```bash
python manage.py loaddata fixtures/initial_data.json
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Collect Static Files

```bash
python manage.py collectstatic
```

### 9. Run Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

## 🔧 Common Issues & Solutions

### Issue: mysqlclient installation fails

**Solution:**
- **macOS:** `brew install mysql-client` then `pip install mysqlclient`
- **Linux:** `sudo apt-get install default-libmysqlclient-dev build-essential`
- **Windows:** Download MySQL Connector/C or use `pip install mysqlclient`

### Issue: Database connection error

**Check:**
1. MySQL server is running
2. Database `ig2026` exists
3. Username and password in `settings.py` are correct
4. Port number matches your MySQL configuration

**Test connection:**
```bash
mysql -u root -p -h localhost -P 3306
```

### Issue: Static files not loading

**Solution:**
```bash
python manage.py collectstatic
```

### Issue: Migration errors

**Solution:**
```bash
# Delete all migration files except __init__.py in core/migrations/
python manage.py makemigrations
python manage.py migrate
```

## 📝 Important Notes

- Default MySQL port in settings is **3306** (change if you use 3307)
- Database name: **ig2026**
- Admin login URL: `/Adminn/`
- Admin dashboard: `/admin-dashboard/`
- Media files are stored in `events/` directory
- Static files are collected in `staticfiles/` directory

## 🔐 Security Reminders

Before deploying:
- Change `SECRET_KEY` in `settings.py`
- Set `DEBUG = False`
- Update `ALLOWED_HOSTS` with your domain
- Use environment variables for sensitive data
- Update email credentials
