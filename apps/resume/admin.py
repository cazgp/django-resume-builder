from django.contrib import admin

from . import models


@admin.register(models.Resume)
class ResumeAdmin(admin.ModelAdmin):
    ordering = ('user__username', 'name')


@admin.register(models.ResumeItem)
class ResumeItemAdmin(admin.ModelAdmin):
    list_display = ('resume', 'title', 'company', 'start_date')

    # user__username will be really inefficient with large amounts of data
    # TODO optimise this ordering
    ordering = ('resume__user__username', 'resume__name', '-start_date')
