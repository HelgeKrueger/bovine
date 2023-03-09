from quart import Blueprint

from .activitypub import activitypub
from .info import info
from .rewrite_request import rewrite_activity_request
from .wellknown import wellknown

default_configuration = Blueprint("default_configuration", __name__)
default_configuration.before_request(rewrite_activity_request)
default_configuration.register_blueprint(wellknown)
default_configuration.register_blueprint(info)
default_configuration.register_blueprint(activitypub)
