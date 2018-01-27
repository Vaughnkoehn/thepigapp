from django.contrib import admin
from pigs.models import *
# Register your models here.

class pigsinline(admin.TabularInline):
    model = Pigsinpen
    


class pigpenadmin(admin.ModelAdmin):
    fieldsets = [
        ('Pigpen', {'fields':['pen']}),
        ]
    inlines = [pigsinline]
    search_fields = ['pen']


class RationAdmin(admin.ModelAdmin):
    readonly_feilds= ('ration_price',)
    

admin.site.register(Pigpen,pigpenadmin)
admin.site.register(Ration,RationAdmin)
admin.site.register(Pigsinpen)
admin.site.register(Shipped)
admin.site.register(pigration)
admin.site.register(deadculled)
admin.site.register(additives)
admin.site.register(Commodity)