from django.contrib import admin
from .models import FolderConfig, EloCategory, LichessFile

admin.site.register(FolderConfig)
admin.site.register(EloCategory)
admin.site.register(LichessFile)
