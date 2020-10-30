from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/", views.random_entry, name="random_entry"),
    path("delete", views.delete, name="delete"),
    path("search", views.search, name="search")
]