from quart import Quart, request

from bovine.wellknown import wellknown

app = Quart(__name__)


def run() -> None:
    app.run()


app.register_blueprint(wellknown)

if __name__ == "__main__":
    run()
