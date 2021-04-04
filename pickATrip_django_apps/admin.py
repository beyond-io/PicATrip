from django.contrib import admin
from commenting_system.models import Comment


# Customized model registration
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'created_on', 'tag', 'commented_post', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('username', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
