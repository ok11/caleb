import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app

app = create_app(config_name=os.getenv('APP_SETTINGS', 'development'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('run', Server(host="0.0.0.0", port=8080))

if __name__ == '__main__':
    manager.run()
