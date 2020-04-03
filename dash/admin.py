from django.contrib import admin
from .models import death, newcase, recovery,deathdetail,testcount,keycountry,indianabroad

# Register your models here.

admin.site.register(death)
admin.site.register(newcase)
admin.site.register(recovery)
admin.site.register(deathdetail)
admin.site.register(testcount)
admin.site.register(keycountry)
admin.site.register(indianabroad)