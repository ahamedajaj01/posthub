# 📝 PostHub — A Simple Django Blog App

PostHub is a Django-based blog application where users can **register, log in, create, edit, delete, and explore posts**.  
Each user can manage only their own posts, while everyone can explore public posts.

---

## 🚀 Features

- ✅ User registration and login
- ✅ Create, view, edit, and delete your own posts
- ✅ Explore all users’ posts
- ✅ Authentication and authorization using Django’s built-in system
- ✅ Safe redirect handling (non-logged users go to login page)
- ✅ Templates protected with `{% if user.is_authenticated %}` blocks


## ⚙️ Installation & Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/posthub.git
   cd posthub
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate       # for Linux/Mac
   venv\Scripts\activate        # for Windows
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Open in browser**
   ```
   http://127.0.0.1:8000/
   ```

---

## 👥 User Authentication Flow

| Action | Access |
|--------|--------|
| **Homepage** | Shows landing page
| **Register** | `/register/` — Create an account |
| **Login** | `/login_view/` — login with email and password |
| **Logout** | `/logout/` — End session |
| **Create Post** | Only for logged-in users |
| **View My Posts** | `/view_post/` — Shows posts authored by the current user |
| **Explore Posts** | `/explore_post/` — Shows all posts |
| **Edit/Delete Post** | Only allowed if the logged-in user is the post’s author |

---

## 🔒 Authorization & Security

- `@login_required(login_url='login_view')` — Protects all sensitive routes  
- Ownership checks in `edit_post` and `delete_post`:
  ```python
  if request.user != post.author:
      messages.error(request, "You are not allowed to edit or delete this post.")
      return redirect('view_post')
  ```
- Template-level restrictions:
  ```html
  {% if user.is_authenticated %}
    <a href="{% url 'view_post' %}">My Posts</a>
  {% else %}
    <a href="{% url 'login_view' %}">Login</a>
  {% endif %}
  ```

---

## 🧩 URL Patterns

```python
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login_view/', views.login_view, name='login_view'),
    path('create_post/', views.create_post, name='create_post'),
    path('view_post/', views.view_post, name='view_post'),
    path('logout/', views.logout_view, name='logout_view'),
    path('explore_post/', views.explore_post, name='explore_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]
```

---

## 🧠 Tips & Notes

- Use Django’s built-in `User` model for authentication.
- Use `messages` framework for user feedback.
- Hide edit/delete buttons from non-owners:
  ```html
  {% if post.author == user %}
      <a href="{% url 'edit_post' post.id %}">Edit</a>
      <a href="{% url 'delete_post' post.id %}">Delete</a>
  {% endif %}
  ```
- For better UX, redirect users back to `next` URL after login.

---

## 🏁 License

This project is open-source and free to use for learning and development purposes.

---

## 💡 Author
**Ajaj Ahamed**  
📧 Email: ahamed.ajaj01@gmail.com
💻 GitHub: [https://github.com/ahamedajaj01](https://github.com/ahamedajaj01)

---

> _“Built with ❤️ using Django and passion for clean code.”_
