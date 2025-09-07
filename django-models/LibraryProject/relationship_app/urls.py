from django.urls import path
from .views import list_books, LibraryDetailView, UserLoginView, UserLogoutView, register

urlpatterns = [
    # existing views
    path("books/", list_books, name="list_books"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # auth views
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
]
