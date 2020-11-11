from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('reg', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('books', views.success),
    path('add_book', views.add_book),
    path('books/<int:book_id>', views.show_book),
    path('update/<int:book_id>', views.update),
    path('un-like/<int:book_id>', views.unlike),
    path('like/<int:book_id>', views.like),
    path('delete/<int:book_id>', views.delete)
]
