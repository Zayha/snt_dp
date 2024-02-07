from django.contrib import admin
from humans.models import News, Category, Voltage


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'image', 'is_published', 'category')
    list_display_links = ('id', 'title', 'time_create')
    search_fields = ('title', 'content')
    ordering = ('-time_create',)
    list_filter = ('id', 'is_published')
    # list_editable = ('is_published',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category)
admin.site.register(Voltage)
admin.site.site_header = 'СНТ "От заката до рассвета"'
