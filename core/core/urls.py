"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home.views import *
from vege.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from api.views import *
urlpatterns = [
    path("", home, name="home"),
    path("failure_page/",failure_page,name="failure_page"),
    path("about/",about,name="about"),
    path("polls/",include("polls.urls")),
    path("recipes/",recipes,name="recipes"),
    path("delete_recipes/<id>/",delete_recipe, name = "delete_recipe"),
    path("update_recipes/<id>/",update_recipe, name = "update_recipe"),
    path("register/",register, name = "register"),
    path("login/",login_page, name = "login"),
    path("logout/",logout_page, name = "logout_page"),
    path('postlist/', post_list, name='post_list'),
    path('postlist/<int:post_id>/', post_detail, name='post_detail'),
    path('create/', create_post, name='create_post'),
    path('api/',handle_initial_route, name='handle_initial_route'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('postlist/edit/<int:post_id>/', edit_post, name='edit_post'),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)
