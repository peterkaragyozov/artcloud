from django.urls import path

from arts.views import list_arts, details_or_comment_art, like_art, edit_art, delete_art, create_art

urlpatterns = [
    path('', list_arts, name='list arts'),

    path('detail/<int:pk>/', details_or_comment_art, name='art details or comment'),
    path('like/<int:pk>/', like_art, name='like art'),

    path('create/', create_art, name='create art'),
    path('edit/<int:pk>/', edit_art, name='edit art'),
    path('delete/<int:pk>/', delete_art, name='delete art'),
]