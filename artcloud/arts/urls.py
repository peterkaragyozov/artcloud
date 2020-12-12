from django.urls import path

from artcloud.arts.views import ArtListView, ArtCreateView, ArtEditView, ArtDeleteView, ArtDetailsView, LikeArtView, CommentArtView

urlpatterns = [
    path('', ArtListView.as_view(), name='list arts'),

    path('detail/<int:pk>/', ArtDetailsView.as_view(), name='art details'),
    path('comment/<int:pk>/', CommentArtView.as_view(), name='comment art'),
    path('like/<int:pk>/', LikeArtView.as_view(), name='like art'),

    path('create/', ArtCreateView.as_view(), name='create art'),
    path('edit/<int:pk>/', ArtEditView.as_view(), name='edit art'),
    path('delete/<int:pk>/', ArtDeleteView.as_view(), name='delete art'),
]
