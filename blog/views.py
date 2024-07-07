from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Blog


# Create your views here.

class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'preview_image', 'is_published',)
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    # отображение публикаций is_published=True
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'preview_image', 'is_published',)
    success_url = reverse_lazy('blog:blog_list')


class BlogDetailView(DetailView):
    model = Blog

    # просмотры
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
