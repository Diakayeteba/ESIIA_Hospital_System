# 🏥 ESIIA Hospital System - Project Instructions

## 🎯 Objective

Build a secure hospital management web application using **Python and Django**.

The system must manage:

* Medical staff (Doctors, Nurses)
* Patients
* Authentication and security (including 2FA)

The application must be:

* Secure
* Role-based
* Scalable
* Cleanly structured

---

## 🏷️ Project Name

**ESIIA Hospital System (EHS)**
Secure hospital management system built with Django.

---

## ⚙️ Tech Stack

* Language: Python
* Framework: Django
* Database: SQLite (default) → scalable to PostgreSQL
* Authentication: Django Auth + 2FA
* Email/SMS: Django Email backend (for OTP)

---

## 🧠 Core Concepts

The system is based on:

* Role-Based Access Control (RBAC)
* Secure Authentication
* Data Privacy (especially patient data)

---

## 👥 User Roles

### 1. Doctor (Admin)

* Full access
* Manage staff (doctors, nurses)
* View and manage patient records
* Modify and delete data

### 2. Nurse

* Can register patients
* Cannot:

  * Edit patients
  * Delete patients
  * View sensitive patient data

### 3. Patient

* Can create account
* Can login securely
* Can view only their own documents
* Has a unique ID

---

## 🔐 Security Requirements

### Authentication Flow

1. User enters username + password
2. System verifies credentials
3. System sends OTP (Email or SMS)
4. User enters OTP
5. Access granted

---

### Password Policy

Password must contain:

* Minimum 10 characters
* Uppercase (A-Z)
* Lowercase (a-z)
* Number (1-9)
* Special character (@, !, $)

---

### Additional Security

* Password hashing (Django default)
* CSRF protection
* Role-based permissions
* Session timeout
* Login attempt limitation
* Secure forms validation

---

## 🧩 Application Modules

### 1. Authentication Module

* Register
* Login
* Logout
* OTP verification
* Password reset

---

### 2. Staff Management Module

* Create doctor
* Create nurse
* Update staff
* Delete staff
* List staff

---

### 3. Patient Management Module

* Register patient (by nurse)
* Generate unique patient ID
* View patient records (doctor only)
* Restrict access based on role

---

### 4. Patient Dashboard

* View personal documents
* Access via unique ID
* Secure session

---

## 🗂️ Project Structure

```
ehs_project/
│
├── accounts/        # Authentication & users
├── staff/           # Doctors & nurses
├── patients/        # Patient management
├── security/        # OTP & 2FA
│
├── templates/
├── static/
│
├── db.sqlite3
├── manage.py
```

---

## 🧱 Models Overview

### User Model (Custom)

* username
* email
* password
* role (Doctor, Nurse, Patient)

---

### Patient Model

* unique_id
* name
* age
* medical_info
* created_by (nurse)

---

### OTP Model

* user
* code
* created_at
* is_valid

---

## 🔄 Key Functional Logic

### Login Flow

* Authenticate user
* Generate OTP
* Send OTP (email/SMS)
* Verify OTP
* Grant access

---

### Access Control Logic

* Doctor → full access
* Nurse → limited access
* Patient → own data only

---

## 🎨 UI Requirements

* Clean and simple interface
* Dashboard per role
* Responsive design
* Secure forms

---

## 🚀 Development Instructions

Follow these steps EXACTLY:

1. Create Django project

2. Create apps:

   * accounts
   * staff
   * patients
   * security

3. Implement custom User model

4. Implement role-based permissions

5. Build authentication system

6. Add OTP system (2FA)

7. Build patient module

8. Build staff module

9. Add templates (HTML)

10. Secure all views

---

## ⚠️ Rules

* DO NOT skip any step
* DO NOT simplify logic
* Follow step-by-step execution
* Write clean and modular code
* Respect Django best practices

---

## 🏁 Expected Outcome

A fully working:

* Secure Django application
* Role-based hospital system
* With 2FA authentication
* Clean architecture

---

## 💡 Bonus Features (Optional)

* Admin dashboard UI
* Activity logs
* Email notifications
* API (Django REST Framework)

---

## 📌 Final Instruction

Execute this file step-by-step like a script.
Do NOT skip or summarize any part.

Build the full system.
