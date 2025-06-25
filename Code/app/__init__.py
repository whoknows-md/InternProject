from flask import Flask, render_template
from app.admin.routes import admin_bp
from app.user.routes import user_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecurekey"  # Replace for production

    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(user_bp, url_prefix="/user")
    
    
    @app.route("/")
    def home():
        return render_template("home.html")

    return app

