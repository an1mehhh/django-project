from django.db import models
from django.template.defaultfilters import slugify
from django.utils.text import get_valid_filename

NULLABLE = {'blank': True, 'null': True}


# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=200, unique=True, **NULLABLE)
    content = models.TextField(verbose_name="Cодержимое", **NULLABLE)
    preview_image = models.ImageField(upload_to='image_blog/', verbose_name="Изображение", **NULLABLE)
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)

#    def save(self, *args, **kwargs):
#    """формирование и проверка slug (по ТЗ нужно реализовать во view.py, здесь альтернативный вариант)"""
#        if not self.slug:
#            self.slug = slugify(get_valid_filename(self.title))
#            original_slug = self.slug
#            queryset = Blog.objects.all().filter(slug__iexact=self.slug).count()
#
#            #добавляет count если будет найдена такая же slug
#            count = 1
#            while queryset:
#                self.slug = f'{original_slug}-{count}'
#                count += 1
#                queryset = Blog.objects.all().filter(slug__iexact=self.slug).count()
#
#        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} {self.content} {self.preview_image} {self.is_published}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ('title', 'content', 'preview_image', 'is_published',)
