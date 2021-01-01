from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('refreshtoken/', jwt_views.TokenRefreshView.as_view(), name='token-refresh'),
    path('public/', views.UnprotectedView.as_view(), name='public-view'),
    path('secret/', views.ProtectedView.as_view(), name='secret-view'),

]

router = DefaultRouter()
router.register('', views.UserViewSet, basename='user')
urlpatterns += router.urls
