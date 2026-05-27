from django.contrib import admin
from .models import Section, Page, PageVersion, AccessRight


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'author', 'created_at', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['is_published', 'section']
    search_fields = ['title', 'content']


@admin.register(PageVersion)
class PageVersionAdmin(admin.ModelAdmin):
    list_display = ['page', 'edited_by', 'edited_at', 'comment']
    list_filter = ['edited_at']


@admin.register(AccessRight)
class AccessRightAdmin(admin.ModelAdmin):
    list_display = ['user', 'section', 'role']
    list_filter = ['role']
