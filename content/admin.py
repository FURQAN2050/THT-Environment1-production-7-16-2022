from django.contrib import admin
from django.forms import ModelForm, ValidationError

from .models import Image
from .models import Video
from .models import Media
from .models import Content
from .models import Tag
from .models import Document


# Register your models here.

class ContentAdmin(admin.ModelAdmin):

    exclude = ('media',)
    search_fields = ['name','sortOrder']
    list_display = ('name','sortOrder')
    def name(self, obj):
        return str(obj.name)

    def level(self, obj):
        return str(obj.sortOrder)

    fieldsets = (
        
        (None, {
            'fields': ('name', 'description', 'tags','sortOrder')
        }),

        ('Add Media', {
            'classes': ('collapse',),
            'fields': ('image_content', 'video_content', 'doc_content'),
        }),

        )

class ImageAdmin(admin.ModelAdmin):

    exclude = ('date', 'added_by','thumbnail',)
    
    def get_readonly_fields(self, request, obj=None):
        
        if obj: # obj is not None, so this is an edit
            return ['image_field', 'name',] # Return a list or tuple of readonly fields' names
        else: # This is an addition
            return []

    def save_model(self, request, obj, form, change):

        obj.added_by = request.user
        super().save_model(request, obj, form, change)


class VideoAdminForm(ModelForm):

    ACCEPTED_FORMATS = ['mp4']

    class Meta:
        model = Video
        fields = '__all__'

    
    # def clean_video_field(self):

    #     video_field = self.cleaned_data['video_field']

    #     if video_field.name[-3:] not in self.ACCEPTED_FORMATS:
    #         raise ValidationError("Video format is incorrect. Only the following formats are supported: " + str(self.ACCEPTED_FORMATS))
        
    #     return video_field
    

class VideoAdmin(admin.ModelAdmin):

    form = VideoAdminForm
    exclude = ('date', 'added_by','thumbnail','video_field_old')

    def get_readonly_fields(self, request, obj=None):
        
        if obj: # obj is not None, so this is an edit
            return ['video_field', 'name',] # Return a list or tuple of readonly fields' names
        else: # This is an addition
            return []

    def save_model(self, request, obj, form, change):

        obj.added_by = request.user
        super().save_model(request, obj, form, change)

class DocAdmin(admin.ModelAdmin):

    exclude = ('date', 'added_by','thumbnail',)

    def save_model(self, request, obj, form, change):

        obj.added_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Document, DocAdmin)
admin.site.register(Media)
admin.site.register(Tag)
admin.site.register(Content, ContentAdmin)