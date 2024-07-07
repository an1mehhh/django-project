from django.urls import path

from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('create/', BlogCreateView.as_view(), name='blog_form'),
    path('edit/<int:pk>/<slug:slug>', BlogUpdateView.as_view(), name='blog_update'),
    path('detail/<int:pk>/<slug:slug>', BlogDetailView.as_view(), name='blog_detail'),
    path('delete/<int:pk>/<slug:slug>', BlogDeleteView.as_view(), name='blog_delete'),

]
