from flask import Flask, jsonify, request
from flask_cors import CORS

from database import DEFAULT_DATABASE_PATH, create_timer, get_timers


def create_app(database_path=DEFAULT_DATABASE_PATH):
    app = Flask(__name__)
    app.config["DATABASE_PATH"] = database_path
    CORS(app)

    @app.get("/api/health")
    def health():
        return jsonify("This is first endpoint!!!!")

    @app.get("/api/timers")
    def list_timers():
        timers = get_timers(app.config["DATABASE_PATH"])
        return jsonify([timer.to_dict() for timer in timers])

    @app.post("/api/timers")
    def add_timer():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Request body must be a JSON object."}), 400

        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            return jsonify({"error": "Name must be a non-empty string."}), 400

        duration_seconds = data.get("duration_seconds")
        if (
            isinstance(duration_seconds, bool)
            or not isinstance(duration_seconds, int)
            or duration_seconds <= 0
        ):
            return jsonify({"error": "duration_seconds must be a positive integer."}), 400

        timer = create_timer(
            name.strip(),
            duration_seconds,
            app.config["DATABASE_PATH"],
        )
        return jsonify({"timer": timer.to_dict()}), 201

    return app


app = create_app()


if __name__ == "__main__":
    app.run(port=5000, debug=True, use_reloader=False)