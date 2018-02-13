from django.contrib import admin
from pigs.models import *
# Register your models here.

class pigsinline(admin.TabularInline):
    model = Pigsinpen
   
class pigletinline(admin.TabularInline):
    model = piglets

class operationiline(admin.TabularInline):
    model = pigletoperation

class pigpenadmin(admin.ModelAdmin):
    fieldsets = [
        ('Pigpen', {'fields':['pen']}),
        ]
    inlines = [pigsinline]
    search_fields = ['pen']

class RationAdmin(admin.ModelAdmin):
    readonly_feilds= ('ration_price',)
    
class sowadmin(admin.ModelAdmin):
    inlines = [pigletinline]

class pigletadmin(admin.ModelAdmin):
    inlines = [operationiline]

admin.site.register(Pigpen,pigpenadmin)
admin.site.register(Ration,RationAdmin)
admin.site.register(Pigsinpen)
admin.site.register(Shipped)
admin.site.register(pigration)
admin.site.register(deadculled)
admin.site.register(additives)
admin.site.register(Commodity)
admin.site.register(Sows, sowadmin)
admin.site.register(piglets,pigletadmin)
admin.site.register(boars)
admin.site.register(operation)