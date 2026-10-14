import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env")
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-local-key-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", os.environ.get("DEBUG", "False")).lower() == "true"
ALLOWED_HOSTS = [x.strip() for x in os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if x.strip()]
INSTALLED_APPS = [
 "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions",
 "django.contrib.messages","django.contrib.staticfiles","rest_framework","rest_framework_simplejwt.token_blacklist",
 "corsheaders","drf_spectacular","authentication","cards","transactions","audit_logs"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware","corsheaders.middleware.CorsMiddleware",
 "django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware",
 "django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware",
 "django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF="config.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR / "templates"],"APP_DIRS":True,
 "OPTIONS":{"context_processors":["django.template.context_processors.debug","django.template.context_processors.request",
 "django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="config.wsgi.application"
DATABASES={"default":{"ENGINE":"django.db.backends.mysql","NAME":os.environ.get("DB_NAME","credit_card_payment_db"),
 "USER":os.environ.get("DB_USER","payment_app"),"PASSWORD":os.environ.get("DB_PASSWORD",""),
 "HOST":os.environ.get("DB_HOST","127.0.0.1"),"PORT":os.environ.get("DB_PORT","3306"),
 "OPTIONS":{"charset":"utf8mb4","connect_timeout":5},"CONN_MAX_AGE":60}}
AUTH_PASSWORD_VALIDATORS=[{"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
 {"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},
 {"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},
 {"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"}]
LANGUAGE_CODE="en-us"; TIME_ZONE="Asia/Kolkata"; USE_I18N=True; USE_TZ=True
STATIC_URL="static/"; STATICFILES_DIRS=[BASE_DIR / "static"]; DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
REST_FRAMEWORK={"DEFAULT_AUTHENTICATION_CLASSES":("rest_framework_simplejwt.authentication.JWTAuthentication",),
 "DEFAULT_PERMISSION_CLASSES":("rest_framework.permissions.IsAuthenticated",),
 "DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",
 "DEFAULT_PAGINATION_CLASS":"rest_framework.pagination.PageNumberPagination","PAGE_SIZE":10,
 "DEFAULT_THROTTLE_CLASSES":["rest_framework.throttling.AnonRateThrottle","rest_framework.throttling.UserRateThrottle"],
 "DEFAULT_THROTTLE_RATES":{"anon":"30/min","user":"120/min"}}
SIMPLE_JWT={"ACCESS_TOKEN_LIFETIME":timedelta(minutes=10),"REFRESH_TOKEN_LIFETIME":timedelta(days=1),
 "ROTATE_REFRESH_TOKENS":True,"BLACKLIST_AFTER_ROTATION":True,"AUTH_HEADER_TYPES":("Bearer",)}
SPECTACULAR_SETTINGS={"TITLE":"Credit Card Payment System API","DESCRIPTION":"Demo-only simulated payments.","VERSION":"1.0.0","SERVE_INCLUDE_SCHEMA":False}
CORS_ALLOWED_ORIGINS=[]
SECURE_CONTENT_TYPE_NOSNIFF=True; X_FRAME_OPTIONS="DENY"
