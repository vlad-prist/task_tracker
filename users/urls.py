from django.urls import path
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from users.views import UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

user_create = UserViewSet.as_view({'post': 'create'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})
user_update = UserViewSet.as_view({
    'put': 'update',
    'patch': 'partial_update'
})
user_delete = UserViewSet.as_view({'delete': 'destroy'})


urlpatterns = [
    path('register/', user_create, name='register'),
    path('detail/<int:pk>/', user_detail, name='user-detail'),
    path('update/<int:pk>/', user_update, name='user-update'),
    path('delete/<int:pk>/', user_delete, name='user-delete'),
] + router.urls
