from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from datetime import datetime

from config import Config

from data_loader import (
    load_history,
    clean_records
)

from model_training import TrafficModel

from traffic_memory import TrafficMemory

from forecasting import forecast_all

from what_if_engine import run_scenarios

from validation import validate_input

from routes import google_route


app = Flask(__name__)

app.config.from_object(
    Config
)


# -----------------------------
# LOAD DATA
# -----------------------------

history = clean_records(
    load_history(
        Config.DATA_FILE
    )
)


# -----------------------------
# TRAIN MODEL
# -----------------------------

model = TrafficModel()

model.fit(
    history
)


# -----------------------------
# TRAFFIC MEMORY
# -----------------------------

memory = TrafficMemory(
    history
)


# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def index():

    return render_template(
        "index.html",

        google_maps_key=
            Config.GOOGLE_MAPS_API_KEY
    )


# -----------------------------
# HEALTH CHECK
# -----------------------------

@app.route(
    "/api/health",
    methods=["GET"]
)
def health():

    return jsonify({

        "ok":
            True,

        "history_rows":
            len(history),

        "model_ready":
            model.ready
    })


# -----------------------------
# HISTORICAL DATA
# -----------------------------

@app.route(
    "/api/history",
    methods=["GET"]
)
def get_history():

    return jsonify(
        history[-120:]
    )


# -----------------------------
# TRAFFIC ANALYSIS
# -----------------------------

@app.route(
    "/api/analyze",
    methods=["POST"]
)
def analyze():

    payload = (
        request
        .get_json(
            silent=True
        )
        or {}
    )


    try:

        data = validate_input(
            payload
        )

    except ValueError as error:

        return jsonify({

            "error":
                str(error)

        }), 400


    # Current traffic state

    current = (
        memory
        .make_current_snapshot(
            data
        )
    )


    # Future prediction

    forecast = forecast_all(

        model,

        memory,

        current
    )


    # Historical matching

    ghost = (
        memory
        .similar_pattern(
            current
        )
    )


    # What-if simulations

    scenarios = run_scenarios(

        current,

        forecast
    )


    return jsonify({

        "current":
            current,

        "forecast":
            forecast,

        "ghost":
            ghost,

        "scenarios":
            scenarios,

        "model": {

            "type":
                model.name,

            "trained_rows":
                len(history)
        },

        "timestamp":
            datetime.now()
            .isoformat(
                timespec="seconds"
            )
    })


# -----------------------------
# GOOGLE ROUTES
# -----------------------------

@app.route(
    "/api/route",
    methods=["POST"]
)
def route_api():

    payload = (
        request
        .get_json(
            silent=True
        )
        or {}
    )


    origin = payload.get(
        "origin"
    )

    destination = payload.get(
        "destination"
    )


    if not origin or not destination:

        return jsonify({

            "error":
                "Origin and destination are required."
        }), 400


    result = google_route(

        origin,

        destination,

        Config.GOOGLE_MAPS_API_KEY
    )


    return jsonify(
        result
    )


# -----------------------------
# START SERVER
# -----------------------------

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True
    )