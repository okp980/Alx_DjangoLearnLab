from django.urls import path
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('update/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('delete/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
]