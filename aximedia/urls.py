from django.conf.urls import url
# from django.conf.urls import include
from django.contrib import admin
from todo import views as todo_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^register/$', todo_views.RegistrationView.as_view(),
        name="registration"),
    url(r'^login/$', todo_views.LoginView.as_view()),
    url(r'^logout/$', todo_views.LogoutView.as_view()),

    url(r'^todos/$', todo_views.ToDoView.as_view()),
    url(r'^todos/(?P<todo_id>\d+)/$',
        todo_views.TasksView.as_view()),
    url(r'^todos/(?P<todo_id>\d+)/task/(?P<task_id>\d+)/$',
        todo_views.SpecificTaskView.as_view()),

]
