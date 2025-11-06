# 📝 Task Management System

A feature-rich **Task Management web application** built with **Django**, designed to help teams manage and track tasks efficiently.

---

## 👨‍💻 About This Project

This is the **first full-stack Django project** I built while learning Django from scratch.  
It served as my **learning-by-building** journey — where I explored Django core features, custom user models, role-based permissions, class-based views, forms, signals, and more.

> 🔀 **Note:** This repository contains **10 development branches**, used to experiment and learn various Django features.  
These branches are **not yet merged** with the `main` branch.  
Also, there is currently **no `requirements.txt`** file — it will be added later after dependency freeze.

---

## 🚀 Features

- 🔐 Custom User model (with profile image and bio)
- ✅ Role-based access (Manager / Employee)
- 📋 Create, assign, and track tasks
- 📌 Task Priority & Status (Pending / In Progress / Completed)
- 📂 Projects linked with tasks
- ✉️ Email notifications on task assignment
- 📊 Manager dashboard with statistics
- 👤 Employee dashboard
- 🧩 Django signals for real-time task logic
- 🧪 Django Debug Toolbar integration

---

## 🧰 Tech Stack

- **Framework:** Django 5.1.4
- **Database:** PostgreSQL
- **Language:** Python
- **Email:** SMTP (Gmail)
- **Environment Config:** `python-decouple`

---

## 📁 Project Structure

task_management/  
&emsp;├── core/  
&emsp;│  
&emsp;├── task/ – Task-related logic and UI  
&emsp;│&emsp;├── models.py  
&emsp;│&emsp;├── views.py  
&emsp;│&emsp;└── forms.py  
&emsp;│  
&emsp;├── user/ – Custom user management  
&emsp;│&emsp;└── models.py (CustomUser)  
&emsp;│  
&emsp;├── media/ – Uploaded files  
&emsp;├── static/ – Static assets (CSS, JS)  
&emsp;├── templates/ – HTML templates  
&emsp;│  
&emsp;├── .env – Environment variables  
&emsp;├── manage.py – Django project runner  
&emsp;└── requirements.txt – Project dependencies  

## 🔐 Permissions Matrix

| Role     | View      | Create | Edit | Delete |
| -------- | --------- | ------ | ---- | ------ |
| Admin    | ✅         | ✅      | ✅    | ✅      |
| Manager  | ✅         | ✅      | ✅    | ✅      |
| Employee | ✅ (Own)   | ❌      | ❌    | ❌      |

## 📬 Contact

**Developer:** Anisul Alam  
**Email:** [anisulalam2003@gmail.com](mailto:anisulalam2003@gmail.com)  
