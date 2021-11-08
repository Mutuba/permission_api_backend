import re

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Role, Permission


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    # allow_blank=True, to enable `" "` as a valid value for a password so as to customize the validation error message,
    # allow_null=True, enable `Null`/`None` as a valid value for a password
    password = serializers.CharField(
        max_length=128, write_only=True, allow_blank=True, allow_null=True
    )

    # Ensure emails are not longer than 128 characters,
    # allow_blank=True, to enable `" "` as a valid value for a email so as to customize the validation error message,
    # allow_null=True, enable `Null`/`None` as a valid value for a email
    email = serializers.EmailField(max_length=128, allow_blank=True, allow_null=True)

    # Ensure username are not longer than 128 characters,
    # allow_blank=True, to enable `" "` as a valid value for a username so as to customize the validation error message,
    # allow_null=True, enable `Null`/`None` as a valid value for a username
    username = serializers.CharField(max_length=128, allow_blank=True, allow_null=True)

    def validate_email(self, data):
        """Validate the email address"""
        email = data
        if email == "":
            raise serializers.ValidationError("Email field is required.")
        elif User.objects.filter(email=email):
            raise serializers.ValidationError(
                "This email is not available. Please try another."
            )
        return data

    def validate_username(self, data):
        """Validate the username"""
        username = data
        if username == "":
            raise serializers.ValidationError("Username field is required.")
        elif User.objects.filter(username=username):
            raise serializers.ValidationError(
                "This username is not available. Please try another."
            )
        return data

    def validate_password(self, data):
        """Validate the password"""
        password = data
        # Ensure passwords are not empty.
        if password == "":
            raise serializers.ValidationError("Password field is required.")
        # Ensure passwords are longer than 8 characters.
        elif len(password) < 8:
            raise serializers.ValidationError(
                "Create a password at least 8 characters."
            )
        # Ensure passwords contain a number.
        elif not re.match(r"^(?=.*[0-9]).*", password):
            raise serializers.ValidationError(
                "Create a password with at least one number."
            )
        # Ensure passwords contain an uppercase letter.
        elif not re.match(r"^(?=.*[A-Z])(?!.*\s).*", password):
            raise serializers.ValidationError(
                "Create a password with at least one uppercase letter"
            )
        # Ensure passwords contain a special character
        elif re.match(r"^[a-zA-Z0-9_]*$", password):
            raise serializers.ValidationError(
                "Create a password with at least one special character."
            )
        return data

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ["email", "username", "password", "token"]

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    # allow_blank=True, to enable `" "` as a valid value for a password so as to customize the validation error message,
    # allow_null=True, enable `Null`/`None` as a valid value for a password
    password = serializers.CharField(
        max_length=128, write_only=True, allow_blank=True, allow_null=True
    )

    # Ensure emails are not longer than 128 characters,
    # allow_blank=True, to enable `" "` as a valid value for a email so as to customize the validation error message,
    # allow_null=True, enable `Null`/`None` as a valid value for a email
    email = serializers.EmailField(max_length=128, allow_blank=True, allow_null=True)

    # Ensure username are not longer than 128 characters,
    # allow_blank=True, to enable `" "` as a valid value for a username so as to customize the validation error message,
    # allow_null=True, enable `Null`/`None` as a valid value for a username
    username = serializers.CharField(max_length=128, allow_blank=True, allow_null=True)
    
    role = serializers.CharField(max_length=128, allow_blank=True, allow_null=True)

    def validate_email(self, data):
        """Validate the email address"""
        email = data
        if email == "":
            raise serializers.ValidationError("Email field is required.")
        elif User.objects.filter(email=email):
            raise serializers.ValidationError(
                "This email is not available. Please try another."
            )
        return data

    def validate_username(self, data):
        """Validate the username"""
        username = data
        if username == "":
            raise serializers.ValidationError("Username field is required.")
        elif User.objects.filter(username=username):
            raise serializers.ValidationError(
                "This username is not available. Please try another."
            )
        return data

    def validate_password(self, data):
        """Validate the password"""
        password = data
        # Ensure passwords are not empty.
        if password == "":
            raise serializers.ValidationError("Password field is required.")
        # Ensure passwords are longer than 8 characters.
        elif len(password) < 8:
            raise serializers.ValidationError(
                "Create a password at least 8 characters."
            )
        # Ensure passwords contain a number.
        elif not re.match(r"^(?=.*[0-9]).*", password):
            raise serializers.ValidationError(
                "Create a password with at least one number."
            )
        # Ensure passwords contain an uppercase letter.
        elif not re.match(r"^(?=.*[A-Z])(?!.*\s).*", password):
            raise serializers.ValidationError(
                "Create a password with at least one uppercase letter"
            )
        # Ensure passwords contain a special character
        elif re.match(r"^[a-zA-Z0-9_]*$", password):
            raise serializers.ValidationError(
                "Create a password with at least one special character."
            )
        return data
    def validate_role(self, role):
        if role not in ["admin", "moderator", "member", "guest"]:
            raise serializers.ValidationError(f"{role} is not a valid role.")
        return role
    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ["id", "email", "username", "password", "role"]

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user_with_role(**validated_data)
    
class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    password = serializers.CharField(
        max_length=128, write_only=True, required=False
    )
    email = serializers.EmailField(max_length=128, required=False)

    username = serializers.CharField(max_length=128, required=False)
    
    role = serializers.CharField(max_length=128, required=False)

    def validate_email(self, data):
        """Validate the email address"""
        email = data
        if email == "":
            return
        elif User.objects.filter(email=email):
            raise serializers.ValidationError(
                "This email is not available. Please try another."
            )
        return data

    def validate_username(self, data):
        """Validate the username"""
        username = data
        if username == "":
            return
        elif User.objects.filter(username=username):
            raise serializers.ValidationError(
                "This username is not available. Please try another."
            )
        return data

    def validate_password(self, data):
        """Validate the password"""
        password = data
        # Ensure passwords are not empty.
        if password == "":
            return
        # Ensure passwords are longer than 8 characters.
        elif len(password) < 8:
            raise serializers.ValidationError(
                "Create a password at least 8 characters."
            )
        # Ensure passwords contain a number.
        elif not re.match(r"^(?=.*[0-9]).*", password):
            raise serializers.ValidationError(
                "Create a password with at least one number."
            )
        # Ensure passwords contain an uppercase letter.
        elif not re.match(r"^(?=.*[A-Z])(?!.*\s).*", password):
            raise serializers.ValidationError(
                "Create a password with at least one uppercase letter"
            )
        # Ensure passwords contain a special character
        elif re.match(r"^[a-zA-Z0-9_]*$", password):
            raise serializers.ValidationError(
                "Create a password with at least one special character."
            )
        return data
    def validate_role(self, role):
        if role == "":
            return
        if role not in ["admin", "moderator", "member", "guest"]:
            raise serializers.ValidationError(f"{role} is not a valid role.")
        return role

    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "role"]

    def update(self,instance,  validated_data):
        instance.__dict__.update(**validated_data)
        return UserSerializer(instance)
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get("email", None)
        password = data.get("password", None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError("An email address is required to log in.")

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError("A password is required to log in.")

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found."
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag to tell us whether the user has been banned
        # or otherwise deactivated. This will almost never be the case, but
        # it is worth checking for. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {"email": user.email, "username": user.username, "token": user.token}


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    token = serializers.CharField(max_length=255, required=False)

    def validate(self, payload):
        check_user = User.objects.filter(email=payload.get("email", None)).first()
        if not check_user:
            raise serializers.ValidationError("Email does not exist")
        token = default_token_generator.make_token(check_user)
        return {"email": payload["email"], "token": token}


class RolePermissionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ["id", "name", "role"]

    def get_role(self, instance):
        return instance.role.name


class StringListField(serializers.ListField):
    child = serializers.CharField()


class RoleSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=255,
        required=True,
        validators=[UniqueValidator(queryset=Role.objects.all())],
    )
    permissions = StringListField(required=True)

    class Meta:
        model = Role
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ["id", "name", "permissions"]

    def validate_name(self, name):
        if name not in ["admin", "moderator", "member", "guest"]:
            raise serializers.ValidationError(f"{name} is not a valid role.")
        return name

    def validate_permissions(self, permissions):
        for permission in permissions:
            if permission in [
                permission.name for permission in Permission.objects.all()
            ]:
                raise serializers.ValidationError(f"{permission} is not unique.")
        return permissions

    def create(self, validated_data):
        role = Role.objects.get(id=3)
        for permission_name in validated_data["permissions"]:
            Permission.objects.create(name=permission_name, role=role)

        return {
            "id": role.id,
            "name": role.name,
            "permissions": [
                permission for permission in role.permissions.all() if permission.active
            ],
        }


class RolesSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    permissions = RolePermissionSerializer(read_only=True, many=True)

    class Meta:
        model = Role
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ["id", "name", "permissions"]


class RoleUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False)
    permissions = RolePermissionSerializer(read_only=True, many=True)

    class Meta:
        model = Role
        fields = ["id", "name", "permissions"]

    def validate_name(self, name):
        if name not in ["admin", "moderator", "member", "guest"]:
            raise serializers.ValidationError(f"{name} is not a valid role.")
        return name

    def update(self, instance, data):
        instance.__dict__.update(**data)
        return RoleUpdateSerializer(instance).data


class PermissionSerializer(serializers.ModelSerializer):
    name = StringListField(required=True, write_only=True)
    role = serializers.CharField(
        required=False,
    )

    class Meta:
        model = Permission
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ["id", "name", "role"]

    def validate_name(self, name):
        for name in name:
            if name in [permission.name for permission in Permission.objects.all()]:
                raise serializers.ValidationError(f"{name} is not unique.")
        return name

    def to_representation(self, value):
        return RoleUpdateSerializer(value).data

    def get_name(self, instance):
        return instance.name

    def create(self, validated_data):
        role = self.context["role"]
        for permission_name in validated_data["name"]:
            Permission.objects.create(name=permission_name, role=role)
        return role

class PermissionUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Permission
        fields = ["id", "name"]

    def validate_name(self, name):
        for name in name:
            if name in [permission.name for permission in Permission.objects.all()]:
                raise serializers.ValidationError(f"{name} is not unique.")
        return name

    def update(self, instance, data):
        instance.__dict__.update(**data)
        return PermissionUpdateSerializer(instance).data