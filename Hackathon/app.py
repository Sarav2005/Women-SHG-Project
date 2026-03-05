import json
import os

from flask import Flask, render_template, request, g, redirect, url_for
from flask_login import LoginManager, current_user

from config import Config
from models import db, User
from auth import auth_bp
from admin import admin_bp
from user import user_bp


def load_translations():
    base_dir = os.path.join(os.path.dirname(__file__), "static", "assets")
    translations = {}
    for lang in ("en", "ta"):
        path = os.path.join(base_dir, f"{lang}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                translations[lang] = json.load(f)
        else:
            translations[lang] = {}
    return translations


translations_cache = load_translations()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_request
    def set_language():
        lang = request.args.get("lang") or request.cookies.get("lang") or "en"
        if lang not in app.config["LANGUAGES"]:
            lang = "en"
        g.lang = lang
        g.t = translations_cache.get(lang, {})

    @app.context_processor
    def inject_globals():
        def t(key):
            return g.t.get(key, key)

        return {
            "current_user": current_user,
            "lang": getattr(g, "lang", "en"),
            "t": t,
        }

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)

    # >>> ROUTE IS DEFINED *INSIDE* create_app, but after app is created
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            if current_user.is_admin():
                return redirect(url_for("admin.admin_dashboard"))
            return redirect(url_for("user.user_dashboard"))
        return redirect(url_for("auth.login"))

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        os.makedirs(os.path.join(os.path.dirname(__file__), "instance"), exist_ok=True)
        from flask_migrate import Migrate

        Migrate(app, db)
        db.create_all()
    app.run(debug=True,port=8000)
