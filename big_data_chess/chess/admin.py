from django.contrib import admin
from .models import BaseFolderConfig, FolderConfig, EloCategory, LichessFile, LichessStatus

class FolderConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Key', {
            'fields': ('env',)
        }),
        ('Local Folder', {
            'fields': ('download_folder', 'unzip_folder')
        }),
        ('Big Folder', {
            'fields': ('split_folder', 'commented_folder', 'reduced_folder', 'archive_folder')
        }),
        ('Target Folder', {
            'fields': ('workflow_folder',)
        }),
    )

    list_display = ('env', 'download_folder')


admin.site.register(FolderConfig, FolderConfigAdmin)
admin.site.register(BaseFolderConfig)
admin.site.register(EloCategory)
admin.site.register(LichessFile)
admin.site.register(LichessStatus)
