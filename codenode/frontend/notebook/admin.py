from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from codenode.frontend.notebook.models import Notebook, Cell



class CellAdmin(admin.ModelAdmin):
    list_display = ('owner', 'type', 'last_modified')
    search_fields = ('owner__username', 'owner__first_name', 'owner__last_name')

admin.site.register(Cell, CellAdmin)


class CellInline(admin.TabularInline):
    """Inline for showing cells in the notebook page"""
    model = Cell
    extra = 0
    fields = ('type', 'content', )
    

class NotebookAdmin(admin.ModelAdmin):
    list_display = ('title', 'system', 'owner', 'created_time')
    search_fields = ('owner__username', 'owner__first_name', 'owner__last_name')
    inlines = [CellInline]

admin.site.register(Notebook, NotebookAdmin)

