"""Admin configuration for Prediction app"""

from django.contrib import admin
from prediction.models import PredictionHistory

@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'predicted_price', 'actual_price')
    list_filter = ('timestamp',)
    search_fields = ('input_data',)
    readonly_fields = ('timestamp', 'input_data', 'predicted_price')
    
    fieldsets = (
        ('Prediction Details', {
            'fields': ('timestamp', 'predicted_price', 'actual_price')
        }),
        ('Input Features', {
            'fields': ('input_data',)
        }),
    )
