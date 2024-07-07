from django.contrib import admin

from blog.models import Blog


# Register your models here.


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'is_published', 'view_count',)
    list_filter = ('created_at', 'is_published')
    search_fields = ('title', 'is_published')
