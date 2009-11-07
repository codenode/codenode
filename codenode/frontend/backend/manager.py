
from django.db import models

class RPCInstanceManager(models.Manager):
    """
    """

    def runInstance(self, backend, type, notebook):
        """The instance_id comes from the actual rpc call.
        Get the owner is the same as the notebook owner.
        """
        


class InstanceManager(RPCInstanceManager):
    """
    General Instance manager class to be used in the EngineInstance Model.
    This allows the implementation to be changed later without affecting
    the model code...
    """

