# OYO Clone Server

\
*An hotel booking platform with vendor and user management, built with Django, Redis, and MySQL.*

## 🚀 Features

### 🏨 Hotel Management

- Vendors can **list their hotels**, including details like amenities, pricing, and images.
- **Dashboard** for vendors to manage bookings, earnings, and hotel performance.
- Redis optimization for efficient database querying and caching.

### 👤 User Management

- **User registration & login** via email authentication.
- Users can **browse hotels, check availability, and book rooms**.
- **Booking history & cancellations** management for users.
- Secure authentication and **role-based access control**.

### 📊 Vendor Management

- **Vendor registration & login** with email verification.
- Vendors can **add, edit, and delete hotels**.
- **View and manage hotel performance, bookings, and user interactions.**

### 🔧 Admin Management

- **Admin panel for monitoring and managing users, vendors, and bookings.**
- **Advanced analytics and reporting features.**
- **Manage system-wide settings and configurations.**

## 🏗️ Low-Level Design (LLD)

- **User Authentication:** Django's built-in authentication with custom user roles.
- **Booking System:** Tracks available rooms, booked dates, and cancellations.
- **Database Optimization:** Uses Redis for caching frequently accessed data.
- **Payment Gateway (Future Scope):** Integration with Razorpay/Stripe.

## 📦 Tech Stack

- **Backend:** Python (Django, Django REST Framework)
- **Frontend:** HTML, CSS, JavaScript (Basic template rendering)
- **Database:** MySQL
- **Caching:** Redis
- **Deployment:** Gunicorn, Nginx, DigitalOcean

## 🛠️ Setup Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/bharath036/OYO_CLONE_SERVER.git
   cd OYO_CLONE_SERVER
   ```
2. Create and activate a virtual environment:
   ```sh
   python3 -m venv myprojectenv
   source myprojectenv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```sh
   python manage.py migrate
   ```
5. Run the server:
   ```sh
   python manage.py runserver
   ```

## 📌 ER Diagram



**ER Diagram needs to be updated.**

## 📌 Low-Level Design (LLD)

**LLD needs to be updated.**

## 📌 Contributing

Feel free to fork this repository, raise issues, or submit PRs to improve the project.


---

💡 **Need help?** Feel free to reach out!

