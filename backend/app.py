from flask import Flask, jsonify, request
from flask_cors import CORS

from database import DEFAULT_DATABASE_PATH, Database
from repositories.timer_repository import TimerRepository
from services.timer_service import TimerService


def create_app(database_path=DEFAULT_DATABASE_PATH):
    app = Flask(__name__)
    app.config["DATABASE_PATH"] = database_path
    CORS(app)
    database = Database(database_path)
    timer_repository = TimerRepository(database)
    timer_service = TimerService(timer_repository)

    @app.get("/api/health")
    def health():
        return jsonify("This is first endpoint!!!!")

    @app.get("/api/timers")
    def list_timers():
        timers = timer_service.list_timers()
        return jsonify([timer.to_dict() for timer in timers])

    @app.post("/api/timers")
    def add_timer():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Request body must be a JSON object."}), 400

        try:
            timer = timer_service.create_timer(
                data.get("name"),
                data.get("duration_seconds"),
            )
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        return jsonify({"timer": timer.to_dict()}), 201

    return app


app = create_app()


if __name__ == "__main__":
    app.run(port=5000, debug=True, use_reloader=False)