from django.contrib import admin

from .models import Printjob, Queue

# admin.site.register(Queue)

class QueueAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "created",)

class PrintjobAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "created",)

admin.site.register(Queue, QueueAdmin)
admin.site.register(Printjob, PrintjobAdmin)
