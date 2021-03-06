from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from todo.models import Profile, Task, ToDo, Organization
from todo.serializers import (LoginSerializer, RegistrationSerializer,
                              TaskSerializer, ToDoSerializer)

# TODO: Check all responses


class RegistrationView(APIView):
    """Registration process"""
    permission_classes = ()

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.data
            username = data['email'].split("@")[0]
            u = User.objects.create(username=username)
            u.email = data['email']
            u.set_password(data['password'])
            u.save()
            # org = request.data['organizations']
            # organizations = [Organization.objects.get(
            #     id=i) for i in org.split(",")]
            # profile = Profile.objects.create(user=u,
            # organizations=organizations)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_403_FORBIDDEN)


class AllToDoView(APIView):
    """ The view describing the user's company's todo-lists"""
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        try:
            user_id = request.user.id
            organization_id = Profile.objects.get(
                user=user_id).current_organization_id

            todos = ToDo.objects.filter(organization=organization_id)
            serialize = ToDoSerializer(todos, many=True)
            return Response(serialize.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        todo_name = request.data['name']
        organization_id = Profile.objects.get(
            user=request.user.id).current_organization_id

        organization = Organization.objects.get(id=organization_id)
        ToDo.objects.create(name=todo_name, organization=organization)
        return Response(status=status.HTTP_201_CREATED)


class AllTasksView(APIView):
    """Get all tasks list and add new tasks to a specific todo"""
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, todo_id):
        try:
            organization_id = Profile.objects.get(
                user=request.user.id).current_organization_id
            # Checks whether the todo is in needed company
            todo = ToDo.objects.get(id=todo_id, organization=organization_id)
            serialize = TaskSerializer(
                Task.objects.filter(todo=todo), many=True)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, todo_id):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            try:
                task_name = request.data['task_name']
                organization_id = Profile.objects.get(
                    user=request.user.id).current_organization_id
                todo = ToDo.objects.get(
                    id=todo_id, organization=organization_id)
                task = Task.objects.create(todo=todo, task_name=task_name,
                                           is_done=False)
                task.save()
                tasks_serialized = TaskSerializer(
                    Task.objects.get(id=task.id))
                return Response(tasks_serialized.data,
                                status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class SpecificTaskView(APIView):
    """The view of a specific task of certain todo"""
    permission_classes = (permissions.IsAuthenticated, )

    def check_access(self, request, todo_id):
        try:
            organization_id = Profile.objects.get(
                user=request.user.id).current_organization_id
            # Check whether the todo is in needed company
            ToDo.objects.get(id=todo_id, organization=organization_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, todo_id, task_id):
        self.check_access(request, todo_id)
        try:
            task = Task.objects.get(id=task_id, todo=todo_id)
            task_serialzer = TaskSerializer(task)
            return Response(task_serialzer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, todo_id, task_id):
        self.check_access(request, todo_id)
        try:
            task = Task.objects.get(id=task_id, todo=todo_id)
            task.task_name = request.data['task_name']
            task.save()
            return Response(status=status.HTTP_200_OK)  # Check
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, todo_id, task_id):
        self.check_access(request, todo_id)
        try:
            task = Task.objects.get(id=task_id, todo=todo_id)
            task.delete()
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    """Login process"""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_403_FORBIDDEN)
        email = serializer.data['email']
        password = serializer.data['password']
        username = User.objects.get(email=email).username
        user = authenticate(username=username, password=password)
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Logout"""

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
