from django.contrib import admin

from .models import Project, Tag, Review
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    
admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(Review)