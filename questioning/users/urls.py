from django.urls import path

from questioning.users import views

app_name = "users"
urlpatterns = [
    path("update/", view=views.UserUpdateView.as_view(), name="update"),
    path("redirect/", view=views.UserRedirectView.as_view(), name="redirect"),
    path("<str:username>/", view=views.UserDetailView.as_view(), name="detail"),
]
