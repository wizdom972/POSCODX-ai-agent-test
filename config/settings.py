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
    "expire_minutes": 30,
    "refresh_expire_days": 7,
}

# API 요청 속도 제한
RATE_LIMIT = {
    "default_rpm": 60,          # 일반 엔드포인트: 분당 60회
    "auth_rpm": 10,             # 인증 엔드포인트: 분당 10회 (무차별 대입 방지)
    "upload_rpm": 5,            # 파일 업로드: 분당 5회
}

# 파일 업로드 설정
UPLOAD = {
    "max_size_mb": 10,
    "allowed_types": ["image/jpeg", "image/png", "image/webp", "application/pdf"],
}
