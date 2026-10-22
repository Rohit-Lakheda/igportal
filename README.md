# IG Portal — Django Multi‑Page Site

A ready‑to‑run Django project with pages: Home, Events, Stakeholder Engagement, Capacity‑building, India @ Global Forums, and SIG (with Observer form).

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.8+** (check with `python3 --version`)
- **MySQL Server** (version 8.0 or higher)
- **pip** (Python package manager)
- **virtualenv** (optional but recommended)

## Setup Instructions

### Step 1: Navigate to Project Directory

```bash
cd igportal
```

### Step 2: Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** If you encounter issues installing `mysqlclient`, you may need to install MySQL development libraries:

**macOS:**
```bash
brew install mysql-client
export PATH="/usr/local/opt/mysql-client/bin:$PATH"
pip install mysqlclient
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install default-libmysqlclient-dev build-essential
pip install mysqlclient
```

**Windows:**
Download MySQL Connector/C from MySQL website or use:
```bash
pip install mysqlclient
```

### Step 4: Setup MySQL Database

1. **Start MySQL Server** (if not running)

2. **Create Database:**
```bash
mysql -u root -p
```

Then in MySQL prompt:
```sql
CREATE DATABASE ig2026 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

3. **Import Database (Optional - if you have existing data):**
```bash
mysql -u root -p ig2026 < ../ig-portal.sql
```

### Step 5: Configure Database Settings

Edit `igportal/settings.py` and update the MySQL database configuration if needed:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ig2026',
        'USER': 'root',
        'PASSWORD': 'your_password',  # Update with your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',  # Default MySQL port (change if using 3307)
    }
}
```

**Note:** The current settings show port 3307. Update it to match your MySQL configuration.

### Step 6: Run Migrations

```bash
python manage.py migrate
```

### Step 7: Load Initial Data (Optional)

```bash
python manage.py loaddata fixtures/initial_data.json
```

### Step 8: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### Step 9: Collect Static Files

```bash
python manage.py collectstatic
```

### Step 10: Run Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

Admin Panel: **http://127.0.0.1:8000/admin/**

## Alternative Setup (Using SQLite - For Quick Testing)

If you want to use SQLite instead of MySQL for quick testing:

1. Comment out the MySQL database configuration in `igportal/settings.py`
2. Uncomment the SQLite configuration (it's already there)
3. Skip Step 4 and Step 5
4. Continue from Step 6

## Project Structure

- `core/models.py` — Event, Consultation, ObserverRequest
- `core/forms.py` — ObserverForm
- `core/views.py` — Page views
- `core/urls.py` — Routes for each page
- `templates/` — Base + per‑page templates
- `static/` — CSS/JS/Images (theme applied)
- `fixtures/initial_data.json` — Sample data
- `events/` — Media files (event images, PDFs)
- `meetings/` — Meeting documents (agenda, records)

## Configuration

### Email Settings

The project is configured to use Gmail SMTP. Update email credentials in `igportal/settings.py`:

```python
EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-app-password"
```

### Security Settings

Before deploying to production:

1. Set `DEBUG = False` in `igportal/settings.py`
2. Update `SECRET_KEY` with a secure random key
3. Configure `ALLOWED_HOSTS` with your domain
4. Update database credentials
5. Use environment variables for sensitive data

## Troubleshooting

### MySQL Connection Issues

- Ensure MySQL server is running
- Verify database credentials in `settings.py`
- Check MySQL port (default is 3306, but settings show 3307)
- Test connection: `mysql -u root -p -h localhost -P 3307`

### Static Files Not Loading

- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATICFILES_DIRS` in settings
- Ensure `DEBUG = True` for development

### Migration Issues

- Delete migration files (except `__init__.py`) and run `python manage.py makemigrations` again
- Or reset database and run migrations fresh

## Deployment Notes

- Set `DEBUG=False` and configure `ALLOWED_HOSTS` in `igportal/settings.py`
- Run `python manage.py collectstatic` and serve via Nginx/Apache
- Use a production-ready database (PostgreSQL/MySQL)
- Set up proper environment variables for sensitive data
- Configure HTTPS/SSL certificates
- Set up proper logging and monitoring
