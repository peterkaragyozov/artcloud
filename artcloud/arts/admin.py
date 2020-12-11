from django.contrib import admin
from artcloud.arts.models import Art, Like, Comment


class LikeInline(admin.TabularInline):
    model = Like


class ArtAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'name', 'year')
    list_filter = ('type', 'year')
    inlines = (
        LikeInline,
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'art_id')


admin.site.register(Art, ArtAdmin)
admin.site.register(Like)
admin.site.register(Comment, CommentAdmin)
