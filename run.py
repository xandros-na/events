import os
from app import create_app, db
from config import DevelopmentConfig

app = create_app(os.environ.get('FLASK_SETTINGS') or 'default')

if __name__ == '__main__':
    devel_config = DevelopmentConfig()
    db_uri = devel_config.SQLALCHEMY_DATABASE_URI

    if not os.path.isfile(db_uri):
        with app.app_context():
            db.create_all()
    app.run()
