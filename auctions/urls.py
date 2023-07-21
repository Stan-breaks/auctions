from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new",views.new, name='new'),
    path("listing/<str:list>",views.list_view, name="list"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("add/<int:list_id>/",views.add,name="add"),
    path("remove/<int:list_id>/",views.remove,name="remove"),
    path("close/<int:list>/",views.close,name="close"),
    path("categories",views.categories,name='categories'),
    path("categories/<str:category>/",views.category,name='category')
]
