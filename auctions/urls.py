from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("chooseCategory", views.chooseCategory, name="chooseCategory"),
    path("detalles/<int:id>", views.listingDetails, name="detalles"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("watchlist", views.verWatchlist, name="verWatchlist"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
]
