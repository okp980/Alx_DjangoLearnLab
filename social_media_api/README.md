## Social Media API

### Project Overview

This is a Django REST Framework-based API for a social media application. It supports user registration, authentication, and basic social media features.

---

## Setup Process

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd social_media_api
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

---

## User Registration & Authentication

### Registration

Users can register via the `/accounts/register/` endpoint (or similar, depending on your implementation). Provide a username, email, password, and confirm_password in the request body.

**Example Request:**

```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword",
  "confirm_password": "securepassword"
}
```

### Authentication

Authentication is typically handled via token-based authentication (e.g., JWT or DRF TokenAuth). After registration, users can log in at `/accounts/login/` to receive an authentication token.

**Example Login Request:**

```json
{
  "username": "newuser",
  "password": "securepassword"
}
```

Include the token in the `Authorization` header for subsequent requests:

```
Authorization: Token <your-token>
```

---

## User Model Overview

The user model is based on Django's default `AbstractUser` or a custom user model. It typically includes:

- `username`: Unique identifier for each user
- `email`: User's email address
- `password`: Hashed password
- Additional fields (optional): profile info, avatar, bio, etc.

Refer to `accounts/models.py` for the exact implementation.

---

## Additional Notes

- For API documentation, use tools like [drf-yasg](https://github.com/axnsan12/drf-yasg) or [django-rest-swagger](https://github.com/marcgibbons/django-rest-swagger).
- Make sure to configure authentication settings in `settings.py`.
