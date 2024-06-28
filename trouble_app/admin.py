from django.contrib import admin
from .models import Issue, Comment, Attachment

class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'created_by', 'assigned_to', 'created_at', 'updated_at')
    list_filter = ('status', 'priority', 'assigned_to')
    search_fields = ('title', 'description',  'priority', 'status', 'created_by__username', 'assigned_to__username')
    raw_id_fields = ('assigned_to', 'created_by')
    date_hierarchy = ('created_at')
    ordering = ('-created_at')

admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Attachment)