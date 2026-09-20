def risk_level(score):

    if score < 35:
        return "LOW"

    if score < 60:
        return "MEDIUM"

    if score < 80:
        return "HIGH"

    return "CRITICAL"


def forecast_all(
    model,
    memory,
    current
):

    current_score = model.predict(
        current
    )

    horizons = [
        15,
        30,
        45,
        60
    ]

    points = []

    for minutes in horizons:

        buildup = min(
            18,
            minutes * 0.16
        )

        score = max(
            0,
            min(
                100,
                current_score
                + buildup
            )
        )

        points.append({

            "minutes":
                minutes,

            "risk_score":
                round(
                    score,
                    1
                ),

            "level":
                risk_level(score)
        })


    peak = max(
        points,
        key=lambda x:
            x["risk_score"]
    )


    return {

        "current_score":
            round(
                current_score,
                1
            ),

        "points":
            points,

        "peak_score":
            peak["risk_score"],

        "peak_minutes":
            peak["minutes"],

        "risk":
            risk_level(
                peak["risk_score"]
            )
    }