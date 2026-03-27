"""애플리케이션 설정"""

APP_NAME = "MyService"
DEBUG = False
SECRET_KEY = "change-me-in-production"

DATABASE = {
    "host": "localhost",
    "port": 5432,
    "name": "myservice_db",
    "user": "app_user",
}

JWT = {
    "algorithm": "HS256",
    "expire_minutes": 60,
}
