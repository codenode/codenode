from django.contrib import admin

from codenode.frontend.notebook.models import Notebook, Cell

class NotebookAdmin(admin.ModelAdmin):
    #list_display = ('__unicode__', )
    search_fields = ('owner__username', 'owner__first_name', 'owner__last_name')

admin.site.register(Notebook, NotebookAdmin)

class CellAdmin(admin.ModelAdmin):
    #list_display = ('__unicode__', )
    search_fields = ('owner__username', 'owner__first_name', 'owner__last_name')

admin.site.register(Cell, CellAdmin)

