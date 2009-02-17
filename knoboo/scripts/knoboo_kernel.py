"""
Kernel server
"""

from twisted.scripts import twistd 

from knoboo import config as knoboo_config


def preRun():
    """Get options relavent to twistd from knoboo's config system.
    """
    options = knoboo_config.KernelServerOptions()
    twistd_options = options.get_twistd_options()
    return twistd_options

def run():
    """Load twistd which will then load the rest of knoboo
    """
    twistd_options = preRun()
    config = twistd.ServerOptions()
    config.parseOptions(twistd_options)
    twistd.runApp(config)
        


