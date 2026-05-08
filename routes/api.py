from flask import Flask, jsonify, request

from utils.helper import (
    helper_add_ufw_rule,
    helper_disable_firewall,
    helper_enable_firewall,
    helper_get_status,
    helper_list_ufw_rules,
    helper_remove_ufw_rule,
)


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
        if request.method == "GET":
            return jsonify(helper_list_ufw_rules())
        elif request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"error": "Missing JSON body"}), 400
            port = data["port"]
            protocol = data["protocol"]
            rule = data["rule"]
            if not port or rule is None:
                return jsonify({"error": "Missing required fields"}), 400

            try:
                helper_add_ufw_rule(port=port, protocol=protocol, rule=rule)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            return jsonify({"message": "Added Firewall Rule", "code": 201}), 201
        elif request.method == "DELETE":
            data = request.get_json()
            rule_id = data["id"]
            helper_remove_ufw_rule(rule_id)
            return jsonify({"message": "Removed Firewall Rule", "code": 200}), 200

    @app.route("/api/ufw/status", methods=["GET"])
    def api_get_status():
        try:
            status = helper_get_status()
            return jsonify(status), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/ufw/enable", methods=["POST"])
    def api_enable_firewall():
        try:
            output = helper_enable_firewall()
            return jsonify(
                {"message": "Firewall enabled successfully", "output": output}
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/ufw/disable", methods=["POST"])
    def api_disable_firewall():
        try:
            output = helper_disable_firewall()
            return jsonify(
                {"message": "Firewall disabled successfully", "output": output}
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
