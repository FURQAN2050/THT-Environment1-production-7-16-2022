from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Questions

# Register your models here.

class QuestionsAdmin(admin.ModelAdmin):
    actions = []
    list_display = (
        'question', 'date', 'responses', 'yes', 'no'
        )
    
    search_fields = ['question', 'date']

    fieldsets = [(
        None, {
            'fields':('question', 'date'),
            }
        )]

admin.site.register(Questions, QuestionsAdmin)
