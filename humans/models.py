from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Текст')
    image = models.ImageField(upload_to="images/%Y/%m/%d/", verbose_name='Изображение', blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время корректировки')
    is_published = models.BooleanField(default=False, verbose_name='Публикация')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категории')

    def __str__(self):
        return f"{self.title} {self.time_create.strftime('%d.%m.%Y')}"

    def get_absolute_url(self):
        return reverse('show_news', kwargs={'news_pk': self.pk})

    class Meta:
        verbose_name = 'Новости СНТ'
        verbose_name_plural = 'Новости СНТ'
        ordering = ['-time_create']


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_category', kwargs={'cat_pk': self.pk})

    class Meta:
        verbose_name = 'Категории новостей'
        verbose_name_plural = 'Категории новостей'


class Voltage(models.Model):
    voltage = models.FloatField(blank=False, verbose_name='Напряжение, В')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время записи')

    class Meta:
        verbose_name = 'Напряжение в сети'
        verbose_name_plural = 'Напряжение в сети'
