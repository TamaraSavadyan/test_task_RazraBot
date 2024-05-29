from flask import Flask
from config import Config
from models import db
from schemas import ma
from routes import task_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)

app.register_blueprint(task_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
