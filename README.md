# 📝 Django Todo App

A fully functional **Todo Application** built using the Django framework. This app allows users to manage their tasks efficiently with features like creating, updating, deleting, and marking tasks as completed. The project includes user authentication and leverages Django Rest Framework for API endpoints.

---

## 🌟 Features

- **CRUD** operations for managing tasks
- Mark tasks as completed or pending
- Paginated task listing for large datasets
- Auto-generated API documentation using DRF Spectacular
- PostgreSQL support for the database

---

## 🚀 Tech Stack

- **Backend**: Django 5.0.7, Django REST Framework 3.15.2
- **Database**: PostgreSQL
- **API Docs**: drf-spectacular

---

## 🛠️ Installation

Follow the steps below to set up and run the project locally:

### 1. Clone the repository:
```bash
git clone https://github.com/pooriyaadibrad/Digipay_ToDo_application.git
cd Digipay_ToDo_application
```
### 2. Create virtual environment and install package(dependencies):
```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```
### 3. Configure the database
+ Install PostgreSQL and create a new database.
+ Update the DATABASES configuration in settings.py with your credentials.

```bash
python manage.py migrate
```
### 4. Run the development server:
```bash
python manage.py runserver
```

## 📖 API Endpoints

| Method   | Endpoint             | Description                   |
|----------|----------------------|-------------------------------|
| `POST`   | `/api/auth/login/`   | Login                        |
| `POST`   | `/api/auth/logout/`  | Logout                       |
| `GET`    | `/api/todos/`        | List all tasks (paginated)   |
| `POST`   | `/api/todos/`        | Create a new task            |
| `PUT`    | `/api/todos/<id>/`   | Update an existing task      |
| `DELETE` | `/api/todos/<id>/`   | Delete a task                |
