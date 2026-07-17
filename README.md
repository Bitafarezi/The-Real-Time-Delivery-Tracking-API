# 🚴‍♂️ Delivery Tracking API

A powerful, secure, and scalable RESTful API coupled with a sleek, real-time frontend dashboard designed for delivery and courier tracking management systems. Built with **Django**, **Django REST Framework (DRF)**, and **Tailwind CSS**, this project features robust role-based access control (RBAC), automatic live-polling, real-time order lifecycle filtering, and interactive API documentation powered by **drf-yasg (Swagger & ReDoc)**.

---

## ✨ Key Features

*   **Role-Based Access Control (RBAC):** Leverages DRF's advanced `Permissions` system to ensure secure data boundaries for Customers, Drivers, and Managers.
*   **Dynamic Querysets:** Automatically filters orders based on the authenticated user's role:
    *   **Customer:** Can only view, track, and create orders they have personally placed.
    *   **Driver:** Can only view and manage orders specifically assigned to them or pending in the system.
*   **On-the-Fly Computed Fields:** Uses `SerializerMethodField` to dynamically calculate and return the estimated arrival time (`delivery_duration`) based on the order's status without bloating the database.
*   **Interactive API Documentation:** Full OpenAPI schema integration using `drf-yasg` providing interactive **Swagger UI** and **ReDoc** endpoints for easy API testing.
*   **Real-time Dashboard UI:** A beautiful, responsive frontend built with Tailwind CSS, supporting:
    *   **Order Creation UI:** A sleek, dedicated sidebar form allowing customers to place orders instantly.
    *   **Real-time Polling:** Seamlessly updates the driver dashboard every 5 seconds without manual page refreshes.
    *   **Custom Notifications:** Interactive toast notification system (success, error, info) instead of standard browser alerts.
*   **Modular Architecture:** Implements `ModelViewSet` and `DefaultRouter` to automatically generate clean, standard CRUD endpoints.

---

## 🛠️ Tech Stack

*   **Backend:** Python 3.14+
*   **Framework:** Django 6.0+
*   **API Toolkit:** Django REST Framework (DRF) 3.17+
*   **API Docs:** drf-yasg 1.21+ (Swagger / ReDoc)
*   **Frontend:** Vanilla JS, HTML5, Tailwind CSS (via CDN)
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
source rest-venv/bin/activate   # On Windows: rest-venv\Scripts\activate
```

### 3. Install Dependencies
``` python
pip install -r requirements.txt
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

### 7. Access the Application

Frontend Dashboard: http://127.0.0.1:8000/dashboard/

Interactive API Browser: http://127.0.0.1:8000/api/order/

Swagger API Docs: http://127.0.0.1:8000/swagger/

ReDoc API Docs: http://127.0.0.1:8000/redoc/

Django Admin Panel: http://127.0.0.1:8000/admin/


## 🗺️ API Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/order/` | List all orders (filtered automatically by user role) |
| **POST** | `/api/order/` | Create a new delivery order |
| **GET** | `/api/order/{id}/` | Retrieve details of a specific order |
| **PUT/PATCH** | `/api/order/{id}/` | Update order details or shift its status |
| **DELETE** | `/api/order/{id}/` | Delete an order entry |
| **POST** | `/api/order/{id}/accept/` | Action for a driver to accept a pending order |
| **POST** | `/api/order/{id}/deliver/` | Action for a driver to mark an active order as delivered |


## 📄 Sample JSON Response
When a authorized client hits a GET request on `/api/order/1/`, the dynamic serializer payload outputs as follows:

```json
{
    "id": 1,
    "restaurant_name": "Avli",
    "address": "Andarzgoo street",
    "status": "Pending",
    "created_at": "2026-07-15T23:11:26.026831Z",
    "updated_at": "2026-07-15T23:11:26.026870Z",
    "delivery_duration": "45-60 minutes",
    "customer": 2,
    "driver": 1,
    "customer_profile": {
        "id": 2,
        "user": {
            "id": 2,
            "username": "john123",
            "first_name": "",
            "last_name": "",
            "full_name": "John Doe"
        },
        "role": "customer",
        "phone_number": "+9891280434",
        "address": "Niki street"
    },
    "driver_profile": {
        "id": 1,
        "user": {
            "id": 1,
            "username": "rumi743",
            "first_name": "",
            "last_name": "",
            "full_name": "Rumi Madson"
        },
        "role": "driver",
        "phone_number": "+9891234567",
        "address": "Empire State"
    }
}
```

## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. **Fork** the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a **Pull Request**


#### 💻 Developed with ❤️ by Bita
