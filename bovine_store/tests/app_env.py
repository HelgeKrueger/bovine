from quart import Quart

from bovine_store.blueprint import bovine_store_blueprint

app = Quart(__name__)

app.register_blueprint(bovine_store_blueprint)
