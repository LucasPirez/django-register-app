from django.contrib import admin

# Register your models here.
from .models import User, Day, Professor, ClassName,Comment,Questions

class ClassAdmin(admin.ModelAdmin):
     filter_horizontal = ('asignacion',)
     



admin.site.register(User)
admin.site.register(Day)
admin.site.register(Professor)
admin.site.register(ClassName, ClassAdmin)
admin.site.register(Comment)
admin.site.register(Questions)