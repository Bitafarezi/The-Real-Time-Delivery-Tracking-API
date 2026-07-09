# 🚴‍♂️ Delivery Tracking API

A powerful, secure, and scalable RESTful API designed for delivery and courier tracking management systems. Built with **Django** and **Django REST Framework (DRF)**, this project features robust role-based access control (RBAC) and real-time order lifecycle filtering.

---

## ✨ Key Features

*   **Role-Based Access Control (RBAC):** Leverages DRF's advanced `Permissions` system to ensure secure data boundaries.
*   **Dynamic Querysets:** Automatically filters orders based on the authenticated user's role:
    *   **Customer:** Can only view and track orders they have personally placed.
    *   **Driver:** Can only view and manage orders specifically assigned to them.
*   **On-the-Fly Computed Fields:** Uses `SerializerMethodField` to dynamically calculate and return the estimated arrival time (`delivery_duration`) based on the order's status without bloating the database.
*   **Modular Architecture:** Implements `ModelViewSet` and `SimpleRouter` to automatically generate clean, standard CRUD endpoints.

---

## 🛠️ Tech Stack

*   **Backend:** Python 3.14+
*   **Framework:** Django 6.0+
*   **API Toolkit:** Django REST Framework (DRF) 3.17+
*   **Database:** SQLite (Easily swappable to PostgreSQL/MySQL)

---

## 🚀 Quick Start & Installation

Follow these steps to set up and run the project locally:

### 1. Clone the Repository
```bash
git clone [https://github.com/Bitafarezi/The-Real-Time-Delivery.git](https://github.com/Bitafarezi/The-Real-Time-Delivery.git)
cd Delivery-Tracking-API
```

### 2. Set Up a Virtual Environment
``` python 
python3 -m venv rest-venv
source rest-venv/bin/activate
```

### 3. Install Dependencies
``` python
pip install django djangorestframework django-filter sqlparse markdown
```

### 4.Run Database Migrations
``` python
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin Account)
``` python
python3 manage.py createsuperuser
```

### 6. Start the Development Server
``` python
python manage.py runserver
```

You can now access the interactive API browser at http://127.0.0.1:8000/api/order/.

## 🗺️ API Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/order/` | List all orders (filtered automatically by user role) |
| **POST** | `/api/order/` | Create a new delivery order |
| **GET** | `/api/order/{id}/` | Retrieve details of a specific order |
| **PUT/PATCH** | `/api/order/{id}/` | Update order details or shift its status |
| **DELETE** | `/api/order/{id}/` | Delete an order entry |


## 📄 Sample JSON Response
When a authorized client hits a GET request on /api/order/1/, the dynamic serializer payload outputs as follows:

{
    "id": 1,
    "customer": "John",
    "driver": "Dave",
    "status": "Preparing",
    "delivery_duration": "30-45 minutes",
    "created_at": "2026-07-09T02:18:16Z"
}


## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. **Fork** the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a **Pull Request**