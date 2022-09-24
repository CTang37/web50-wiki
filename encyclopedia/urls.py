from django.urls import path

from . import views

"""
app_name = "encyclopedia"
"""

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("random", views.random, name="random"),
    path("delete", views.delete, name="delete"),
    path("edit/<str:namecap>", views.edit, name="edit"),
    path("<str:name>", views.entry, name="entry"),
]