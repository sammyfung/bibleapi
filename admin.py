from django.contrib import admin
from .models import Version, Book, Bible, Heading


class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'language')
    list_filter = ['language']
    search_fields = ('code', 'name')


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'version', 'name', 'testament')
    list_filter = ['version', 'testament']
    search_fields = ['name']


class BibleAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'chapter', 'verse', 'text')
    search_fields = ('book.version', 'book.name', 'text')


class HeadingAdmin(admin.ModelAdmin):
    list_display = ('id', 'before', 'text')
    search_fields = ('before.book.name', 'text')


admin.site.register(Version, VersionAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Bible, BibleAdmin)
admin.site.register(Heading, HeadingAdmin)
