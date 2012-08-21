"""
Logging functionality for Varda server.

.. moduleauthor:: Martijn Vermaat <martijn@vermaat.name>

.. Licensed under the MIT license, see the LICENSE file.
"""


from flask import g, request
from flask import current_app


def make_logger(base):
    def logger(message, *args, **kwargs):
        header = ''
        if request.remote_addr is not None:
            header = '[ip: %s] ' % request.remote_addr
            if g.user is not None:
                header += '[user: %s] ' % g.user.login
        getattr(current_app.logger, base)(header + message, *args, **kwargs)
    return logger


debug = make_logger('debug')
info = make_logger('info')
warning = make_logger('warning')
error = make_logger('error')
