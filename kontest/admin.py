from django.contrib import admin

from .models import Kontest, Masala, UserKontestRelation, UserMasalaRelation, Test


class TestAdmin(admin.TabularInline):
    model = Test

class MasalaAdmin(admin.ModelAdmin):
    inlines = [TestAdmin]
    list_display = ['title', 'kontest', 'ball', 'is_published']
    search_fields = ['title', 'kontest__title', 'is_published']
    list_filter = ['kontest', 'is_published']

class UserKontestRelationAdmin(admin.ModelAdmin):
    model = UserKontestRelation
    search_fields = ['user__username']
    list_filter= ['kontest']

admin.site.register(Kontest)
admin.site.register(Masala, MasalaAdmin)
admin.site.register(UserKontestRelation, UserKontestRelationAdmin)


class UserMasalaRelationAdmin(admin.ModelAdmin):
    model = UserMasalaRelation
    search_fields = ['user__username']
    list_filter = ['masala','state']

admin.site.register(UserMasalaRelation, UserMasalaRelationAdmin)
# admin.site.register(Test)
