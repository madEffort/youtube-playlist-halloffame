from django.contrib import admin
from .models import Hall, Video


class VideoInline(admin.StackedInline):
    model = Video
    extra = 3

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    inlines = [VideoInline]

@admin.register(Video)
class HallAdmin(admin.ModelAdmin):
    pass