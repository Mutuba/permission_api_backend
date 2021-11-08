from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from .models import Role, Permission, User
from functools import partial
from rest_framework.exceptions import NotFound
from rest_framework import mixins, status, viewsets
from apps.core.permissions import UserHasPermission
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    RoleSerializer,
    RolesSerializer,
    RoleUpdateSerializer,
    PermissionSerializer,
    PermissionUpdateSerializer,
    UserSerializer,
    UserUpdateSerializer
)


class RegistrationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        operation_description="User Registration", operation_id="register_user"
    )
    def post(self, request):
        user = request.data.get("user", {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(operation_description="User Login", operation_id="user_login")
    def post(self, request):
        user = request.data.get("user", {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    By subclassing create, list, retrieve and destroy
    we can define create, list, retrieve and destroy
    endpoints in one class
    """

    queryset = Role.objects.all()
    permission_classes = [
        IsAuthenticated,
        partial(UserHasPermission, "can_create_role"),
    ]
    serializer_class = RoleSerializer
    # pagination_class = LimitOffsetPagination
    @swagger_auto_schema(
        operation_description="Create Role", operation_id="role_create"
    )
    def create(self, request):

        """Creates a new role in the database if it does not exist
        Method takes role data, validates and commits in the db
        """

        serializer_data = request.data

        serializer = self.serializer_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Get Roles List",
        operation_id="roles_list",
        responses={200: RolesSerializer},
    )
    def list(self, request):

        """Retrives all articles from the database"""
        # using self.get_queryset() to avoid cache results
        page = self.paginate_queryset(self.get_queryset())

        serializer = RolesSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class RoleUpdateView(GenericAPIView):
    permission_classes = [
        IsAuthenticated,
        partial(UserHasPermission, "can_create_role"),
    ]
    serializer_class = RoleUpdateSerializer

    @swagger_auto_schema(
        operation_description="Update Role", operation_id="role_update"
    )
    def put(self, request, pk):

        """Creates a new role in the database if it does not exist
        Method takes role data, validates and commits in the db
        """

        try:
            serializer_instance = get_object_or_404(Role, pk=pk)
        except Role.DoesNotExist:

            raise NotFound(f"Role with id {pk} does not exist.")

        serializer_data = request.data
        serializer = RoleUpdateSerializer(data=serializer_data)
        if serializer.is_valid(raise_exception=True):
            serializer_result = serializer.update(serializer_instance, serializer_data)
            return Response(serializer_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PermissionCreateView(GenericAPIView):
    permission_classes = [
        IsAuthenticated,
        partial(UserHasPermission, "can_create_permission"),
    ]
    serializer_class = PermissionSerializer

    @swagger_auto_schema(
        operation_description="Update Role",
        operation_id="create_permission",
        responses={200: RoleSerializer},
    )
    def post(self, request, pk):

        """Creates a new role in the database if it does not exist
        Method takes role data, validates and commits in the db
        """

        try:
            role = get_object_or_404(Role, pk=pk)
        except Role.DoesNotExist:

            raise NotFound(f"Role with id {pk} does not exist.")
        serializer_context = {"role": role}
        serializer_data = request.data
        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PermissionUpdateView(GenericAPIView):
    permission_classes = [
        IsAuthenticated,
        partial(UserHasPermission, "can_create_permission"),
    ]
    serializer_class = PermissionUpdateSerializer

    @swagger_auto_schema(
        operation_description="Update Role",
        operation_id="create_permission",
        responses={200: PermissionUpdateSerializer},
    )
    def put(self, request, pk):

        """Updates a role in the database if it does not exist
        Method takes role data, validates and commits in the db
        """

        try:
            serializer_instance = get_object_or_404(Permission, pk=pk)
        except Role.DoesNotExist:

            raise NotFound(f"Role with id {pk} does not exist.")    
        serializer_data = request.data
        serializer = self.serializer_class(data=serializer_data)
        if serializer.is_valid(raise_exception=True):
            serializer_result = serializer.update(serializer_instance, serializer_data)
            return Response(serializer_result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserCreateView(GenericAPIView):
    permission_classes = [
        IsAuthenticated,
        partial(UserHasPermission, "can_assign_role"),
    ]
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Update Role",
        operation_id="create_user_with_permission",
        responses={200: UserSerializer},
    )
    def post(self, request):

        """Updates a role in the database if it does not exist
        Method takes role data, validates and commits in the db
        """
        serializer_data = request.data
        serializer = self.serializer_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
class UserUpdateView(GenericAPIView):
    permission_classes = [
        IsAuthenticated,
        partial(UserHasPermission, "can_update_user"),
    ]
    serializer_class = UserUpdateSerializer
    @swagger_auto_schema(
        operation_description="Update User",
        operation_id="create_user_details",
        responses={200: UserSerializer},
    )
    def put(self, request, pk):

        """Creates a new role in the database if it does not exist
        Method takes role data, validates and commits in the db
        """

        try:
            serializer_instance = get_object_or_404(User, pk=pk)
        except Role.DoesNotExist:

            raise NotFound(f"Role with id {pk} does not exist.")

        serializer_data = request.data
        serializer = self.serializer_class(data=serializer_data)
        if serializer.is_valid(raise_exception=True):
            serializer_result = serializer.update(serializer_instance, serializer_data)
            return Response(serializer_result.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)