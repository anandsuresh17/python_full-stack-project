# Scope India

A Django-based training and student enrollment platform focused on course promotion, student registration, email verification, profile management, and course enrollment workflows.

This project was reviewed directly from the workspace code and reflects only the behavior implemented in the current application.

## Project Overview

This project is a Django web application built around the MVT (Model-View-Template) architecture. It serves as a student-facing portal for technology training programs, allowing users to:

- browse course offerings
- register as a student
- verify their email address
- sign in to a personal dashboard
- manage profile details
- change/reset password
- search available courses
- enroll in and remove courses
- contact the training institute

The app is organized into two Django apps:

- `apps1` for the public site, registration, authentication, and enrollment flow
- `dashb` for the authenticated dashboard and student account management

## Key Features

The following features are implemented in the current codebase:

- Student registration form with validation
- Email verification after registration
- First-login password creation flow
- Forgot password and reset link flow
- Change password functionality
- Student profile display and profile editing
- Course listing and dashboard enrollment management
- Course search with AJAX/JSON response
- Contact form with email sending
- Course-specific landing pages for Python, Java, MERN, React, Testing, UI/UX, and Data Analytics
- SQLite database setup
- Media upload for profile images

## Technologies Used

The project currently uses the following technologies and packages, verified from the active project environment:

- Python
- Django 6.0.7
- SQLite
- HTML, CSS, and Django templates
- Pillow for image handling
- python-dotenv for environment variables
- requests for external country/state/city API calls
- SMTP email via Gmail configuration

A `requirements.txt` file was not present in the current workspace review, so dependencies were verified from the active virtual environment instead.

## MVT Architecture

This project follows the Django MVT pattern:

### Model

Models are defined in `apps1/models.py` and include:

- `Students` — stores student profile information, verification status, and uploaded image
- `CoursesList` — stores available course metadata such as name, duration, and fee
- `Profile` — links a Django `User` to the student profile system
- `CourseEnrollment` — records course enrollments and prevents duplicate enrollment per profile/course
- `Contact` — stores contact form submissions

These models are the application data layer and are used by the views to read/write database records.

### View

Views live in:

- `apps1/views.py` for public pages, registration, login, verification, password flow, and country/state/city JSON endpoints
- `dashb/views.py` for authenticated dashboard actions, profile management, enrollment, search, and password changes

Views handle request processing, validation, database access, email sending, authentication, and rendering responses.

### Template

Templates are stored in the `templates/` folder and are rendered using Django template language. Examples include:

- `home.html`
- `registration.html`
- `login.html`
- `sd.html`
- `profile.html`
- `edit_profile.html`
- `change_password.html`
- `forgot_password.html`
- `new_password.html`
- `newpass.html`
- course pages such as `python.html`, `java.html`, `mern.html`, etc.

The shared layout is defined in `templates/layout.html`.

### URL Routing and Request Flow

A typical request follows this lifecycle:

URL → View → Model → Template → Response

Example:

1. A user visits `/registration/`
2. The matching URL route calls the `registrationpage` view
3. The view validates form data and creates a `User` + `Students` record
4. The view sends an email verification link
5. Django renders the `registration.html` or `login.html` template with a message
6. The browser receives the final response

This pattern is used throughout the project for registration, login, course enrollment, profile management, and password operations.

## Django Apps and Their Responsibilities

### `apps1`

This is the main app for the public experience and account lifecycle.

Responsibilities include:

- homepage and static pages
- student registration
- login/logout flow
- email verification
- first-time password setup
- password reset and forgot password logic
- contact form submission
- course-specific landing pages
- external country/state/city data JSON endpoints

### `dashb`

This app handles the authenticated dashboard and student management features.

Responsibilities include:

- displaying available courses
- allowing course signup and removal
- filtering/searching courses via AJAX
- rendering the profile page
- editing profile information
- changing passwords
- sending password reset emails from the logged-in user flow

## Database and Models

The project uses SQLite as configured in `myproject/settings.py`.

The main models are:

### `Students`

Stores:

- linked Django `User`
- first name and last name
- email
- gender
- date of birth
- contact number
- country, state, city
- hobbies as a JSON array
- image upload
- `first_login` flag
- `email_verified` flag

### `CoursesList`

Stores:

- course name
- duration
- fee

### `Profile`

Links a Django `User` to a profile record used in enrollment logic.

### `CourseEnrollment`

Stores a mapping between a `Profile` and a `CoursesList` record, with a unique constraint to prevent duplicate enrollment entries for the same course.

### `Contact`

Stores information submitted from the contact form.

## Authentication and User Management

This project uses Django's built-in authentication system with the default `User` model.

Implemented behavior includes:

- user creation during student registration
- login using email as the username
- `@login_required` protection on dashboard-related views
- session expiry support (`keep_logged_in` option)
- logout action
- custom first-login password requirement

Students are linked to a Django `User` via a one-to-one relationship in the `Students` model.

## Email Verification

Email verification is implemented during registration.

Flow:

1. A new student is created with a Django `User` entry.
2. A temporary password is generated.
3. A signed token is created using Django's `signing.dumps()`.
4. A verification link is emailed to the student.
5. The user clicks the link and the project verifies the token using `signing.loads()`.
6. The student's `email_verified` field is set to `True`.

The verification token is time-limited with `max_age=86400` (24 hours). Invalid or expired tokens display a message on the login page.

## Password Change and Password Reset

### Password Change

Users can change their password from the profile area.

The implemented logic checks:

- current password validity
- matching new and confirm passwords
- updates the Django user password
- logs the user out afterward

### Password Reset

The project includes two reset patterns:

- `forgot_password` for a user who knows their email and wants a temporary password
- `reset_password_email` for sending a token-based password reset email when the user is already logged in

The password reset token is generated using Django's `default_token_generator` and is sent via email.

## Student Profile Management

Student profile management is implemented in the dashboard area.

Users can:

- view their personal information
- edit profile details
- update country, state, and city values
- upload or replace profile image
- review hobbies and other information stored in the model

The `profile.html` template presents the profile in a card layout, while `edit_profile.html` provides the update form.

## Course Search and Enrollment

Course enrollment is implemented in the dashboard (`sd.html`).

Features include:

- listing all available courses from `CoursesList`
- displaying the student's enrolled courses
- enrollment via `signup_course`
- removing an enrollment via `delete_course`
- searching courses by name using a text input

Course search uses a Django view that filters by `course_name__icontains` and returns a JSON payload. The frontend uses the browser `fetch()` API to update the course table without a full page reload.

## AJAX / JSON Functionality

AJAX and JSON are used in the project for the following flows:

- `search_courses` in `dashb/views.py` returns course results as JSON
- `get_countries`, `get_states`, and `get_cities` in `apps1/views.py` return JSON data from the external CountriesNow API
- the dashboard search input uses `fetch()` to retrieve live course results

The project also has a `static/js/` directory in the workspace, but it is currently empty. The implemented frontend AJAX behavior in the inspected code is included directly in the `sd.html` template.

## Project Structure

```text
finalproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps1/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── dashb/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── templates/
│   ├── layout.html
│   ├── home.html
│   ├── login.html
│   ├── registration.html
│   ├── sd.html
│   ├── profile.html
│   ├── edit_profile.html
│   ├── change_password.html
│   ├── forgot_password.html
│   ├── new_password.html
│   ├── newpass.html
│   ├── contact.html
│   ├── about.html
│   ├── python.html
│   ├── java.html
│   ├── mern.html
│   ├── react.html
│   ├── testing.html
│   ├── uiux.html
│   └── data_analytics.html
├── static/
│   ├── css/
│   ├── images/
│   └── js/
├── media/
│   └── documents/
├── db.sqlite3
├── myenv/
├── Readme.md
└── .env (not committed in this project review)
```

> Note: a `requirements.txt` file was not present in the workspace during review. Dependencies were validated from the active environment instead.

## Installation and Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the required packages.
4. Configure environment variables in a `.env` file.
5. Run database migrations.
6. Start the Django development server.

## Virtual Environment Setup

Example commands:

```bash
python -m venv myenv
```

On Windows:

```powershell
myenv\Scripts\activate
```

On macOS/Linux:

```bash
source myenv/bin/activate
```

Install the required dependencies:

```bash
pip install Django==6.0.7 pillow==12.3.0 python-dotenv==1.2.3 requests==2.34.2
```

## Environment Variables

Environment variables are loaded from a project-level `.env` file using `python-dotenv`.

The current project reads the following keys in `myproject/settings.py`:

```env
SECRET_KEY=your_secret_key_here
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_app_password
```

Do not commit real credentials to version control. Keep this file local and secure.

## Database Migration

Run the project migrations:

```bash
python manage.py migrate
```

This uses the SQLite database configured in the project settings and creates the application tables.

## Running the Development Server

Start the app locally with:

```bash
python manage.py runserver
```

Then open the app in a browser at:

```text
http://127.0.0.1:8000/
```

## Application Workflow

The app workflow implemented in the code is as follows:

1. User visits the landing page and views course categories.
2. User registers a student account.
3. The app creates a Django user and a `Students` record.
4. An email verification link is sent.
5. The user verifies the email and signs in.
6. On first login, the user is asked to create a new password.
7. The user reaches the dashboard and sees available courses.
8. The user searches for a course and can enroll.
9. The user manages profile details and password settings.
10. The user can remove enrollment or sign out.

## Security Considerations

The project includes some basic security patterns, but it is configured for development use and should not be treated as production-ready without additional hardening.

Current observations from the code:

- Django authentication is used (`User`, `login_required`)
- passwords are stored using Django’s standard password hashing
- email verification is required before login
- reset tokens are time-based and sent by email
- environment variables are loaded from `.env` rather than hardcoded in source files
- `DEBUG = True` is enabled in settings
- `ALLOWED_HOSTS = ['*']` is set
- uploaded profile images are stored in the local `media/` directory

For deployment, additional production measures would be necessary, including:

- restricting `ALLOWED_HOSTS`
- disabling `DEBUG`
- securing secret management
- using HTTPS
- hardening SMTP configuration
- reviewing file upload and permission settings

## Future Improvements

These are reasonable next steps, but they are not currently implemented in the codebase:

- add automated unit and integration tests
- separate development and production settings files
- add a formal `requirements.txt` file for easier environment setup
- add more detailed Django admin customizations
- implement course categories or filtering beyond simple search
- add stronger validation and logging for email delivery
- add deployment configuration for a production server
- add more advanced dashboard analytics or reporting

## Author

Anand Suresh

This README reflects the actual implementation present in the current workspace and intentionally avoids claiming features or credentials that are not present in the code.
