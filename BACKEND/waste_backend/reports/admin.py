# reports/admin.py
from django.contrib import admin
from .models import WasteReport

@admin.register(WasteReport)
class WasteReportAdmin(admin.ModelAdmin):
    list_display = ('waste_type', 'user', 'collector', 'status', 'created_at')
    list_filter = ('status', 'collector', 'waste_type')
    search_fields = ('description',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['collector'].queryset = CustomUser.objects.filter(role='collector')
        return form