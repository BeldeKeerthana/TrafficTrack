def run_scenarios(
    current,
    forecast
):

    base_score = forecast[
        "peak_score"
    ]

    scenarios = []

    for diversion in [
        0,
        10,
        20
    ]:

        congestion_reduction = (
            diversion * 0.42
        )

        spillback = (

            0

            if diversion == 0

            else diversion * 0.10
        )

        projected = (

            base_score

            -
            congestion_reduction

            +
            spillback
        )

        projected = max(
            0,
            min(
                100,
                projected
            )
        )

        estimated_travel = (

            8
            +
            projected * 0.12
        )

        diverted = (

            current[
                "vehicles_per_min"
            ]
            *
            diversion
            / 100
        )

        scenarios.append({

            "diversion_percent":
                diversion,

            "projected_congestion":
                round(
                    projected,
                    1
                ),

            "estimated_travel_minutes":
                round(
                    estimated_travel,
                    1
                ),

            "vehicles_diverted_per_min":
                round(
                    diverted,
                    1
                ),

            "status":

                "BASELINE"

                if diversion == 0

                else "SIMULATED"
        })


    return scenarios