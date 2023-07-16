from django.contrib import admin
from .models import Question

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question','order','points')
    search_fields = ['question','order']

admin.site.register(Question,QuestionAdmin);