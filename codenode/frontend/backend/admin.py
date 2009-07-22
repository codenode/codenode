from django.contrib import admin

from codenode.frontend.backend.models import BackendServer
from codenode.frontend.backend.models import EngineType
from codenode.frontend.backend.models import EngineInstance

class BackendServerAdmin(admin.ModelAdmin):
    """
    """

admin.site.register(BackendServer, BackendServerAdmin)

class EngineTypeAdmin(admin.ModelAdmin):
    """
    """

admin.site.register(EngineType, EngineTypeAdmin)

class EngineInstanceAdmin(admin.ModelAdmin):
    """
    """

admin.site.register(EngineInstance, EngineInstanceAdmin)
