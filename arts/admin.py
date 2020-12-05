from django.contrib import admin
from arts.models import Art, Like, Comment


class LikeInLine(admin.TabularInline):
    model = Like


admin.site.register(Art)
admin.site.register(Like)
admin.site.register(Comment)
