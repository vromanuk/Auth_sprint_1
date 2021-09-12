from src import create_app
from src.database.db import db_session

app = create_app()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run()
