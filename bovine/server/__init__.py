from quart import Blueprint

from .activitypub import activitypub
from .activitypub_client import activitypub_client
from .info import info
from .wellknown import wellknown

default_configuration = Blueprint("default_configuration", __name__)
default_configuration.register_blueprint(wellknown)
default_configuration.register_blueprint(info)
default_configuration.register_blueprint(activitypub)
default_configuration.register_blueprint(activitypub_client)
