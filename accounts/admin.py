from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone

from pytz.reference import UTC
import pytz
import datetime

from .models import Districts, Teacher, Teams, Subscriptions, School, User

# Register your models here.

class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'teachers'

class UserAdmin(BaseUserAdmin):
    inlinesTeacher = (TeacherInline,)
    inlinesDistrictManager = []

    list_display = ('username', 'email', 'first_name', 'last_name', 'active','subscriptionType', 'get_points', 'last_login','teacher_school','team','date_joined','district')
    search_fields = ['username', 'email', 'first_name', 'last_name', 'teacher__subscriptionType__name','teacher__points','teacher__school__name','teacher__team__team','teacher__district__district']

    def get_points(self, obj):
        return obj.teacher.points
    
    def get_inline_instances(self, request, obj=None):
        if obj != None:
            if obj.isDistrictManager == False:
                return [inline(self.model, self.admin_site) for inline in self.inlinesTeacher]
        
            return [inline(self.model, self.admin_site) for inline in self.inlinesDistrictManager]

    def good_until(self, obj):

        return obj.teacher.goodUntil

    def teacher_school(self, obj):

        return obj.teacher.school

    def team(self, obj):

       return obj.teacher.team
    
    def district(self, obj):

       return obj.teacher.district

    def active(self, obj):

        central = pytz.timezone("US/Central")

        if obj.teacher.goodUntil != None:

            # Convert datetime.date to datetime.datetime
            goodUntilDate = datetime.datetime.fromordinal(obj.teacher.goodUntil.toordinal())

            if central.localize(goodUntilDate) > timezone.now():
                return True

        return False

    def subscriptionType(self, obj):

       return obj.teacher.subscriptionType

    good_until.admin_order_field = 'teacher__goodUntil'
    get_points.admin_order_field = 'teacher__points'
    teacher_school.admin_order_field='teacher__school'
    team.admin_order_field='teacher__team'
    # district.admin_order_field='teacher__district'

class DistrictAdmin(admin.ModelAdmin):
    search_fields = ['district']
    exclude = ('points', 'participants', 'historyPoints')
    def district(self, obj):
        return str(obj.district)

class TeamsAdmin(admin.ModelAdmin):

    list_display = (
        'team', 'school', 'get_points', 'get_num_participants','get_teacher'
    )

    search_fields = ['team', 'school__name', 'school__district__district']

    fieldsets = [(None, {'fields':('team', 'school', 'color')})]


class SchoolAdmin(admin.ModelAdmin):

    search_fields = ['name', 'district__district']

admin.site.register(Districts, DistrictAdmin)
admin.site.register(Teams, TeamsAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Subscriptions)
admin.site.register(School, SchoolAdmin)


