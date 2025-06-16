from django.contrib import admin

from scmtracker.models import ModerationStream, PostModeration

admin.site.register(ModerationStream)
admin.site.register(PostModeration)