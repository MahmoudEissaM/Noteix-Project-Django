# MyNotes - Personal Note Management System

![MyNotes Logo](https://img.shields.io/badge/MyNotes-Personal%20Notes%20App-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📝 Overview

MyNotes is a comprehensive web application built with Django that allows users to create, manage, and organize personal notes. The application provides a secure environment for users to store important information, categorize notes, and even archive sensitive content behind PIN protection.

## ✨ Features

- **User Authentication**: Secure registration and login system
- **Dashboard**: Intuitive interface to manage all your notes
- **Note Categories**: Organize notes into categories (Important, Tasks, Study, Personal)
- **Archiving System**: PIN-protected archive for sensitive notes
- **Profile Management**: Customize your profile with images and personal information
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Technology Stack

- **Backend**: Django 5.2
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Bootstrap 5
- **Form Handling**: Django Widget Tweaks
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Django's built-in authentication system

## 📋 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mynotes.git
cd mynotes
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

## 🔧 Project Structure

```
mynotes_project/
├── manage.py
├── mynotes_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── notes/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   │   ├── notes/
│   │   │   ├── add_note.html
│   │   │   ├── archive.html
│   │   │   ├── dashboard.html
│   │   │   └── ...
│   │   └── registration/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static/
├── media/
├── templates/
└── requirements.txt
```

## 📱 Application Workflow

1. **Registration/Login**: Users start by creating an account or logging in
2. **Dashboard**: Main interface for viewing and managing notes
3. **Note Creation**: Users can create notes with titles, content, categories, and optional links
4. **Note Management**: Edit, delete, or change categories of existing notes
5. **Archiving**: Move sensitive notes to a PIN-protected archive
6. **Profile Management**: Update profile information and profile picture

## 🔐 Security Features

- Password hashing using Django's authentication system
- PIN-protected archive for sensitive notes
- CSRF protection for all forms
- Session management for secure user sessions

## 🌟 Future Enhancements

- Note sharing functionality
- Rich text editor for note content
- Mobile application
- Dark mode support
- Export/import notes functionality
- Email notifications and reminders

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

- **Your Name** - [GitHub Profile](https://github.com/yourusername)

## 🙏 Acknowledgements

- Django Documentation
- Bootstrap Team
- All open-source contributors whose libraries made this project possible

---

Feel free to contribute to this project by submitting issues or pull requests!
