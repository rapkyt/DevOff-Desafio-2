from django.urls import path

from app.devoff import views

app_name = "devoff"
urlpatterns = [
    path("encrypt", views.encrypt, name="encrypt"),
    path("decrypt", views.decrypt, name="decrypt"),
]
