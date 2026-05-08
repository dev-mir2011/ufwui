from flask import Flask, render_template


def frontend_routes(app: Flask):
    @app.route("/")
    def index():
        return render_template("index.html")
