import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'car_rental_db')
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'car_rental_secret_key')
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Payment Gateway
    PAYMENT_GATEWAY_KEY = os.getenv('PAYMENT_GATEWAY_KEY', '')
    PAYMENT_GATEWAY_SECRET = os.getenv('PAYMENT_GATEWAY_SECRET', '')
    
    # Upload
    UPLOAD_FOLDER = 'static/car_images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
