import os
from app import create_app, db
from config import config

app = create_app(os.environ.get('FLASK_SETTINGS') or 'default')

if __name__ == '__main__':

    db_uri = config['default'].SQLALCH_DB_URI
    print(db_uri)
    if not os.path.isfile(db_uri):
        with app.app_context():
            db.create_all()

    app.run()
