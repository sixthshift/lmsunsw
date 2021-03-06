"""
Customizations for the Django administration interface
"""
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils import six
from django.apps import apps
from django.contrib.admin import widgets
from django.conf import settings
from django.shortcuts import render, redirect

from app.models import *
from app.forms import (LectureAdminForm, QuizAdminForm, QuizChoiceInLineForm, 
CodeSnippetAdminForm, ThreadAdminForm, QuickSettingsForm, LectureMaterialInLineFormset)

###################################################################################################

# Admin settings for staff

class CustomUserAdmin(UserAdmin):
    list_display = ('username','email', 'first_name', 'last_name')

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            return ((None, {'fields': ('username', 'password')}),(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),)
        else:
            return super(CustomUserAdmin, self).get_fieldsets(request, obj)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if not request.user.is_superuser:
            object_id = unicode(request.user.id)

        return super(CustomUserAdmin, self).change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            return redirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=(request.user.id,)))
        return super(CustomUserAdmin, self).changelist_view(request=request, extra_context=extra_context)

class QuizChoiceInLine(admin.StackedInline):
    model = QuizChoice
    # no min since quiz can be freeform
    min_num = 0
    # display none in beginning to simplify display
    extra = 0
    # override admin css styling for inputs
    def formfield_for_dbfield(self, db_field, *args, **kwargs):
        if db_field.name == 'choice':
            kwargs['widget'] = widgets.AdminTextInputWidget({'id': 'admin-form-control', 'class': 'form-control', 'placeholder': 'One of the quiz choices'})
        return super(QuizChoiceInLine, self).formfield_for_dbfield(db_field, *args, **kwargs)

class QuizAdmin(admin.ModelAdmin):
    """
    the admin view for creating and editing quizzes, including quiz chocies
    """
    inlines = [QuizChoiceInLine]
    form = QuizAdminForm
    fieldsets = (
        ('Quiz Question', {
            'fields': ('question', 'visible', 'Lecture','answer')
            }
        ),
        ('Code Snippet', {
            'fields': ('syntax', 'code')
            }
        ),
    )

class LectureMaterialInLine(admin.StackedInline):
    model = LectureMaterial
    extra = 0
    min_num = 1
    formset = LectureMaterialInLineFormset

    def formfield_for_dbfield(self, db_field, *args, **kwargs):
        if db_field.name == 'online_lecture_material':
            kwargs['widget'] = widgets.AdminTextInputWidget({'id': 'admin-form-control', 'class': 'form-control'})
        return super(LectureMaterialInLine, self).formfield_for_dbfield(db_field, *args, **kwargs)

class LectureAdmin(admin.ModelAdmin):
    form = LectureAdminForm
    inlines = [LectureMaterialInLine]


class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('__unicode__','personal_collab_doc','seat_location')
    fieldsets = (
        (None, {
            'fields': ('personal_collab_doc',)
            }
        ),

    )

    # should not be able to create or delete any, must be done in conjunction with User model
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # once user profile has been made, you should not be able to change the FK
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if not request.user.is_superuser:
            object_id = unicode(request.user.UserProfile.id)
        self.exclude = ('user',)
        return super(UserProfileAdmin, self).change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            return redirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=(request.user.UserProfile.id,)))
        return super(UserProfileAdmin, self).changelist_view(request=request, extra_context=extra_context)

class CodeSnippetAdmin(admin.ModelAdmin):
    form = CodeSnippetAdminForm

class PostsInLine(admin.StackedInline):
    model = Post
    exclude = ('rank',)
    min_num = 0
    extra = 0
    def formfield_for_dbfield(self, db_field, *args, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = widgets.AdminTextareaWidget({'id': 'admin-form-control', 'class': 'form-control'})
        return super(PostsInLine, self).formfield_for_dbfield(db_field, *args, **kwargs)


class ThreadAdmin(admin.ModelAdmin):
    inlines = [PostsInLine]
    form = ThreadAdminForm

class Admin_Site(AdminSite):

    def get(self, request, extra_context=None):

        extra_context['quick_settings_form'] = QuickSettingsForm(session=request.session)


    def post(self, request, extra_context=None):
        

        # quick_settings_form is never processed, just used as a placeholder for ajax submissions
        extra_context['quick_settings_form'] = QuickSettingsForm(session=request.session)


    def index(self, request, extra_context=None):
        if not request.user.is_superuser:
            # students should not see the dashboard page
            return redirect('index')
        else:
            extra_context = {} if extra_context==None else extra_context

            # do forms stuff
            if request.method == 'POST':
                self.post(request, extra_context)
            else:
                self.get(request, extra_context)

            return super(Admin_Site, self).index(request, extra_context)

    def app_index(self, request, app_label,extra_context=None):
        # another uneccesary page for students
        if not request.user.is_superuser:
            return redirect('index')
        else:
            return super(Admin_Site, self).app_index(request, app_label, extra_context)

adminsite = Admin_Site()


adminsite.register(User, CustomUserAdmin)
adminsite.register(UserProfile, UserProfileAdmin)
adminsite.register(Quiz, QuizAdmin)
adminsite.register(Lecture, LectureAdmin)
adminsite.register(CodeSnippet, CodeSnippetAdmin)
adminsite.register(Thread, ThreadAdmin)

