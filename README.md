# DailyLines – Blogging Web Application

A full-stack blogging platform built using Django that allows users to create, interact with, and explore blog content.

---

## 🚀 Features

- User authentication (login & signup)
- Create, edit, and delete blog posts (CRUD)
- Like and comment system
- Search functionality
- Category-based post organization
- Pagination for better performance

---

## 🛠 Tech Stack

- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap

---

## 📁 Project Structure

- `blog/` – main application logic  
- `templates/` – HTML files  
- `static/` – CSS and assets  
- `manage.py` – Django management script  

---

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/laxmi2405/DailyLines

# Navigate to project folder
cd DailyLines

# Create virtual environment
python -m venv env

# Activate environment
env\Scripts\activate   (Windows)
# or
source env/bin/activate  (Mac/Linux)

# Install dependencies
pip install -r requirements.txt

# Run server
python manage.py runserver
