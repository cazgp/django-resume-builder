from django.contrib import admin

from . import models


@admin.register(models.ResumeItem)
class ResumeItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'resume_id','resume_name')
    ordering = ['-start_date']

    def resume_id(self, obj):
        return obj.resume.id

    def resume_name(self, obj):
        return obj.resume.name

@admin.register(models.Resume)
class ResumeItem(admin.ModelAdmin):
    list_display = ('user', 'name')
    ordering = ('user', '-name')
