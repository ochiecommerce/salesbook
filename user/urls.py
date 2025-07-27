from django.urls import path, include

from .views import UsernameCheckView, UserSearchView

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("check/", UsernameCheckView.as_view(), name="username_check"),
    path("search/", UserSearchView.as_view(), name="user_search"),
]