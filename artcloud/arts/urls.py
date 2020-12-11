from django.urls import path

from artcloud.arts.views import details_or_comment_art, like_art, ArtListView, ArtCreateView, ArtEditView, ArtDeleteView

urlpatterns = [
    path('', ArtListView.as_view(), name='list arts'),

    path('detail/<int:pk>/', details_or_comment_art, name='art details or comment'),
    path('like/<int:pk>/', like_art, name='like art'),

    path('create/', ArtCreateView.as_view(), name='create art'),
    path('edit/<int:pk>/', ArtEditView.as_view(), name='edit art'),
    path('delete/<int:pk>/', ArtDeleteView.as_view(), name='delete art'),
]
