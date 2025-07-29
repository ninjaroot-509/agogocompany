# Agogo Company

Agogo Company is an e‑commerce demo built with **Django 2.2**.  It provides a simple online shop where visitors can browse products, place items in a basket and checkout using the MonCash payment gateway.

## Features

* **Custom user accounts** – sign up and log in with email using `django-allauth`. Extra profile fields such as address and date of birth are collected on registration.
* **Product catalogue** – create, update and manage `Product` entries.  Each product can receive user reviews and ratings.
* **Shopping basket** – anonymous and registered users can add items to a basket that tracks quantities and totals.
* **Checkout process** – converts the basket to an `Order` and redirects users to MonCash for payment.
* **Order history** – logged-in users can view previous orders and track their status.
* **Basic CMS pages** – a landing page that highlights popular and new products along with a simple About page.

## Installation

1. Create and activate a Python virtual environment.
2. Install the required packages:

   ```bash
   pip install django==2.2.10 django-crispy-forms django-allauth moncashify
   ```
3. Apply database migrations and create a superuser:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Run the development server:

   ```bash
   python manage.py runserver
   ```

The site will be available at `http://localhost:8000/`.

## Running tests

To execute the test suite run:

```bash
python manage.py test
```

## Project layout

The repository is organised into several Django apps:

| App       | Purpose                                     |
|-----------|---------------------------------------------|
| `accounts`| Custom user model and profile forms         |
| `pages`   | Home and About pages                        |
| `products`| Product catalogue and review system         |
| `basket`  | Shopping basket and middleware              |
| `checkout`| Order creation and MonCash integration      |
| `orders`  | Displays order history for a user           |

## License

This project is provided for educational purposes and contains no production secrets.
