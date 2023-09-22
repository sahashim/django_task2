from django.contrib import admin

#from .actions import set_title_test
from .models import *


# Register your models here.


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['author', 'title', 'publish', 'status', 'category', 'is_del']
    ordering = ['title', 'publish']
    list_filter = ['status', 'publish', 'author']
    search_fields = ['title', 'description']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    prepopulated_fields = {"slug": ['title']}
    list_editable = ['status']
    list_display_links = ['title']
    #actions = [set_title_test]
    #set_title_test.short_description = 'set title'





@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['title', 'publish']
    prepopulated_fields = {"slug": ['title']}


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = [ 'writer', 'content', 'post']
