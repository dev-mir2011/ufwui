from flask import Flask, jsonify

from utils.helper import helper_list_ufw_rules


def api_routes(app: Flask):
    @app.route("/api")
    def api():
        routes = []

        for rule in app.url_map.iter_rules():
            if not rule.rule.startswith("/api"):
                continue

            routes.append(
                {
                    "endpoint": rule.endpoint,
                    "methods": list(rule.methods),
                    "path": rule.rule,
                }
            )

        return jsonify(routes)

    @app.route("/api/ufw", methods=["GET", "POST", "DELETE"])
    def api_ufw():
        return jsonify(helper_list_ufw_rules("mir"))
