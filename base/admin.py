from django.contrib import admin
from base.models import Contact, Entry


class NotesAdmin(admin.ModelAdmin):

    list_display = ('title', 'slug', 'created_at', 'updated_at',)

    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Contact)
admin.site.register(Entry)
