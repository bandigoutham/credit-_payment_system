from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from authentication.views import RegisterView, LogoutView, MeView
from cards.views import CardViewSet
from transactions.views import TransactionViewSet, transaction_export, daily_summary
router=DefaultRouter()
router.register("cards",CardViewSet,basename="cards")
router.register("transactions",TransactionViewSet,basename="transactions")
urlpatterns=[
 path("admin/",admin.site.urls),path("api/auth/register/",RegisterView.as_view()),
 path("api/auth/login/",TokenObtainPairView.as_view()),path("api/auth/refresh/",TokenRefreshView.as_view()),
 path("api/auth/logout/",LogoutView.as_view()),path("api/auth/me/",MeView.as_view()),
 path("api/admin/transactions/export.csv",transaction_export),path("api/admin/daily-summary/",daily_summary),
 path("api/",include(router.urls)),path("api/schema/",SpectacularAPIView.as_view(),name="schema"),
 path("api/docs/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui")]
