from django.contrib import admin

from game_app.models import Platform, Game, Image


class PlatformInline(admin.TabularInline):
    model = Game.platforms.through
    extra = 0


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class GameAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'resource_type', 'original_release_date']
    search_fields = ['name']
    list_filter = ['resource_type']
    exclude = ['platforms']

    inlines = [PlatformInline, ImageInline]


class PlatformAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['name']


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Game, GameAdmin)