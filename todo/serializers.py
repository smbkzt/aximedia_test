from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile, Task, ToDo


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def is_valid(self):
        super(RegistrationSerializer, self).is_valid()
        is_user_exists = User.objects.filter(email=self.data['email']).exists()
        if is_user_exists:
            self._errors['email_exists'] = "The email is already in use."
            return False
        return True


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = ('id', 'name')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task_name', 'is_done')


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = Profile
        fields = ('email', 'password', 'current_organization_id',)

    def is_valid(self):
        super(LoginSerializer, self).is_valid()
        try:
            user = User.objects.get(email=self.data['email'])
            if not check_password(self.data['password'], user.password):
                self._errors['invalid_password'] = 'Password is invalid'
                return False

            # Check if the user is in the organization
            organization_id = self.data['current_organization_id']
            organizations = Profile.objects.get(user=user).organizations.all()
            if any(int(organization_id) == o.id for o in organizations):
                # Add flag
                profile = Profile.objects.get(user=user)
                profile.current_organization_id = organization_id
                profile.save()
                return True
            else:
                return False
        except User.DoesNotExist:
            self._errors['no_user'] = 'User does not exist'
            return False
