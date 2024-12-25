# Django REST Framework Applications with Security Features

## Explanation

This project consists of two Django REST Framework (DRF) applications: Sender and Receiver. The goal is to develop secure APIs that facilitate encrypted message transmission between these two apps, as well as integrating essential features. The key features are User Authentication for login and registration functionalities for both apps, a secure messaging using custom middleware to secure data transmissions as security to handle encryption, hashing, and request validation, and a dashboard.

## Prerequisites

-Python 3.12 or higher
-Django 4.0 or higher
-Django REST Framework
-Requests library for testing

How to setup

Clone the repository
Create and activate a virtual environment
Install dependencies
Navigate to each project directory (sender_project and receiver_project) and run migration

Start the servers

Sender:
python manage.py runserver 8000
Receiver:
python manage.py runserver 8001

Testing:

Use the test_messages.py script to test secure message transmission
