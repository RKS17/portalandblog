from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('notes/', views.notes, name='notes'),
    path('delete_note/<int:pk>',views. delete_note, name='delete_note'),
    path('notes_detail/<int:pk>',views.NotesDetailView.as_view(), name='notes-detail'),

    path('homeworks/',views.homework, name='homework'),
    path('update_homework/<int:pk>',views.update_homework, name='update-homework'),
    path('delete_homework/<int:pk>',views.delete_homework, name='delete-homework'),

    path('todo/',views.todo, name='todo'),
    path('update_todo/<int:pk>',views.update_todo, name='update-todo'),
    path('delete_todo/<int:pk>',views.delete_todo, name='delete-todo'),
    path('books/', views.books, name='books'),

    path('blog/', views.blog, name='blog'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    

]