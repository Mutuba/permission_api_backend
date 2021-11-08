from django.urls import path

from .views import (
    LoginAPIView,
    RegistrationAPIView,
    RoleViewSet,
    RoleUpdateView,
    PermissionCreateView,
    PermissionUpdateView,
    UserCreateView,
    UserUpdateView,
)

app_name = "authentication"
urlpatterns = [
    path("users/signup", RegistrationAPIView.as_view(), name="user_create"),
    path("admin/users/create", UserCreateView.as_view(), name="user_signup"),
    # path("admin/users/play/<int:pk>", UserUpdateView.as_view()),
    path("users/login/", LoginAPIView.as_view(), name="user_login"),
    path("roles/", RoleViewSet.as_view({"post": "create"}), name="create_role"),
    path("roles/<int:pk>/update", RoleUpdateView.as_view()),
    path("roles/list/", RoleViewSet.as_view({"get": "list"})),
    path("roles/<int:pk>/", PermissionCreateView.as_view()),
    path("permissions/<int:pk>/", PermissionUpdateView.as_view()),
    path("admin/users/<int:pk>/update", UserUpdateView.as_view()),
]
