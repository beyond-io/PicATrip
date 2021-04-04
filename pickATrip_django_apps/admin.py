from django.apps import apps
from django.contrib import admin


# Customized model registration
@admin.register
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'body', 'created_on', 'tag', 'post', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('username', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


# for viewing models registration fields
class ListAdminMixin(object):
    def __init__(self, general_model, admin_site):
        self.list_display = [field.name for field in general_model._meta.get_fields()]
        super(ListAdminMixin, self).__init__(model, admin_site)


# Register all other models automatically - should stay last in file.
models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
