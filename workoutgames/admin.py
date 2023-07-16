from django.contrib import admin
from django import forms
from .models import Path, Workout, WorkoutPlace, Movement, MovementType, ImageWorkout, VideoWorkout, MediaWorkout, Tag
from django.forms.models import BaseInlineFormSet
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils import timezone
from django.db.models import Q

import datetime as dt
from functools import partial

# Register your models here.

class VideoForm(forms.ModelForm):

    ACCEPTED_FORMATS = ['mp4']

    class Meta:
        model = VideoWorkout
        fields = '__all__'

    def clean(self):
        video = self.cleaned_data.get('video_field')

        if video.name[-3:] not in self.ACCEPTED_FORMATS:
            raise forms.ValidationError("Video format is incorrect. Only the following formats are supported: " + str(self.ACCEPTED_FORMATS))

        return self.cleaned_data

class PathAdmin(admin.ModelAdmin):
    list_display = ('name','levelPath','sortOrder')
    search_fields = ['name','levelPath','sortOrder']

    def name(self, obj):
        return str(obj.name)
    def levelPath(self, obj):
        return str(obj.levelPath)
    def sortOrder(self, obj):
        return str(obj.sortOrder)

    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'description')
    #     }),
    # )

    def get_form(self, request, obj=None, **kwargs):
        kwargs['formfield_callback'] = partial(self.formfield_for_dbfield, request=request, obj=obj)
        return super(PathAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name != "workout":
            kwargs.pop('obj', None)
        return super(PathAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        path = kwargs.pop('obj', None)
        if db_field.name == "workout":
            kwargs["queryset"] = Workout.objects.filter(Q(path__in=[path]) | Q(datePosted__gte=(timezone.now() - dt.timedelta(minutes=30))))
        return super(PathAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

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


class VideoAdmin(admin.ModelAdmin):

    form = VideoForm

    exclude = ('date', 'added_by','thumbnail',)
    
    def get_readonly_fields(self, request, obj=None):
        
        if obj: # obj is not None, so this is an edit
            return ['video_field', 'name',] # Return a list or tuple of readonly fields' names
        else: # This is an addition
            return []

    def save_model(self, request, obj, form, change):

        obj.added_by = request.user
        super().save_model(request, obj, form, change)


class WorkoutPlaceInlineFormset(BaseInlineFormSet):

    def checkIfDuplicates(self, listOfElems):
        ''' Check if given list contains any duplicates '''

        for elem in listOfElems:
            if listOfElems.count(elem) > 1:
                return True
        return False

    def clean(self):
    
        super(WorkoutPlaceInlineFormset, self).clean()

        places = []

        for form in self.forms:

            if not form.is_valid():
                return #other errors exist, so don't bother

            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                places.append(form.cleaned_data['place'])

        if len(places) > 2 or self.checkIfDuplicates(places):
            raise forms.ValidationError('Duplicate places exist')

        if len(places) > 1 and WorkoutPlace.PLACE[2][0] in places:
            raise forms.ValidationError('If "Both" is selected, it must be the only workout place')

        if len(places) < 2 and WorkoutPlace.PLACE[2][0] not in places:
            raise forms.ValidationError('Workouts must be selected for both Gym and Home')

     
class MovementInline(GenericTabularInline):
    model = Movement
    extra = 0

class WorkoutPlaceAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        kwargs['formfield_callback'] = partial(self.formfield_for_dbfield, request=request, obj=obj)
        return super(WorkoutPlaceAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name != "movements":
            kwargs.pop('obj', None)
        return super(WorkoutPlaceAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        workoutplace = kwargs.pop('obj', None)
        print(workoutplace)
        if db_field.name == "movements" and workoutplace:
            kwargs["queryset"] = Movement.objects.filter(Q(workoutplace__in=[workoutplace]) | Q(datePosted__gte=(timezone.now() - dt.timedelta(minutes=30))))
        return super(WorkoutPlaceAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

class WorkoutPlaceInline(admin.TabularInline):
    model = WorkoutPlace
    extra = 0
    max_num = 2
    formset = WorkoutPlaceInlineFormset

class WorkoutAdmin(admin.ModelAdmin):

    exclude = ('datePosted',)
    inlines = [WorkoutPlaceInline,]
    list_display = ('name','level')
    search_fields = ['name','level']

    def name(self, obj):
        return str(obj.name)

    def level(self, obj):
        return str(obj.level)

class MovementTypeAdmin(admin.ModelAdmin):
    
    exclude = ('datePosted',)
    list_display = ('name',)

    def name(self, obj):
        return str(obj.name)

    name.admin_order_field = 'name'
    search_fields = ('name',)

class MovementAdmin(admin.ModelAdmin):

    exclude = ('datePosted', )
    list_display = ('name','base_sets','base_reps','base_weight')

    def name(self, obj):
        return str(obj.movement_type.name)

    def base_sets(self,obj):
        return obj.base_sets

    def base_reps(self,obj):
        return obj.base_reps

    def base_weight(self,obj):
        return obj.base_weight

    name.admin_order_field = 'movement_type__name'
    base_sets.admin_order_field = 'base_sets'
    base_reps.admin_order_field = 'base_reps'
    base_weight.admin_order_field = 'base_weight'
    search_fields = ('movement_type__name', 'base_sets', 'base_reps', 'base_weight',)


class TagAdmin(admin.ModelAdmin):

    list_display = ('element',)

    def element(self, obj):
        return str(obj.tag.element)

    element.admin_order_field = 'tag__element'



admin.site.register(ImageWorkout, ImageAdmin)
admin.site.register(VideoWorkout, VideoAdmin)
admin.site.register(MediaWorkout)
admin.site.register(Path, PathAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(WorkoutPlace, WorkoutPlaceAdmin)
admin.site.register(Movement, MovementAdmin)
admin.site.register(MovementType, MovementTypeAdmin)
admin.site.register(Tag)