from quart import Blueprint

from .wellknown import wellknown
from .info import info
from .activitypub import activitypub

default_configuration = Blueprint("default_configuration", __name__)
default_configuration.register_blueprint(wellknown)
default_configuration.register_blueprint(info)
default_configuration.register_blueprint(activitypub)
