# The-Recipe-Room
Another try at a recipe website 

## Overview
> This is a Django-based web application is another try at a recipe website that allows users to  create an account, login, logout, create and post recipe, modify or delete recipes.

## Prerequisites

Before you begin, ensure you have the following software installed on your machine:
- **Python 3.12+**
- **Git**
- **Virtualenv** (Optional but recommended)
- **PostgreSQL** (or any other database)

## Setup Instructions

### 1. Clone the Repository
To get a copy of the project up and running on your local machine, clone the repository:

```bash
git clone https://https://github.com/CiaranBrain/The-Recipe-Room.git
```

Navigate into the project directory:

```bash
cd The-Recipe-Room
```

### 2. Create and Activate a Virtual Environment
It's recommended to use a virtual environment to isolate dependencies. Run the following commands to create and activate it:

#### For Linux/macOS:
```bash
python3 -m venv myenv
source myenv/bin/activate
```

#### For Windows:
```bash
python -m venv myenv
myenv\Scripts\activate
```

### 3. Install Dependencies
With the virtual environment activated, install all required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory of your project to set up environment variables. The `.env` file typically contains sensitive information like database credentials, secret keys, etc.

Example `.env` file:

```bash
SECRET_KEY=your-secret-key
DEBUG=True  # Set to False for production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings for PostgreSQL
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Set Up the Database
Depending on the database you are using, set it up (e.g., PostgreSQL). Then, apply the migrations to create the necessary tables:

```bash
python manage.py migrate
```

If you need to create a superuser (administrator), run:

```bash
python manage.py createsuperuser
```

### 6. Collect Static Files (for Production)
If you're deploying to production, collect static files so they can be served properly:

```bash
python manage.py collectstatic
```

### 7. Run the Development Server
To test that everything is set up correctly, run the Django development server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser to view the app.

## Deployment

### Deploying to a Production Server (Gunicorn + Nginx)
For a production deployment, you'll likely use a combination of **Gunicorn** and **Nginx**.

#### 1. Install Gunicorn:
```bash
pip install gunicorn
```

Run Gunicorn to serve the application:
```bash
gunicorn project_name.wsgi:application
```

#### 2. Configure Nginx:
If you're using **Nginx**, create a configuration file for your site (replace `project_name` and paths as needed):

```bash
server {
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /path/to/static/;
    }

    location /media/ {
        alias /path/to/media/;
    }
}
```

Start/restart Nginx:
```bash
sudo systemctl restart nginx
```

### Deploying on Heroku (Alternative)
If you want to deploy to **Heroku**, follow these steps:

#### 1. Install Heroku CLI:
Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

#### 2. Log in to Heroku:
```bash
heroku login
```

#### 3. Create a Heroku App:
```bash
heroku create
```

#### 4. Set Up Heroku Environment Variables:
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=yourdomain.com
```

#### 5. Push the Code to Heroku:
```bash
git push heroku main
```

#### 6. Apply Migrations on Heroku:
```bash
heroku run python manage.py migrate
```

### Additional Deployment Notes
- Ensure you have proper security settings for production: set `DEBUG = False` in your `.env` file, and configure `ALLOWED_HOSTS`.
- Use HTTPS in production.
- Use a robust database in production (e.g., PostgreSQL).

## License
Include your project's license details here, for example:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **GitHub**: [CiaranBrain](https://https://github.com/CiaranBrain)

---
