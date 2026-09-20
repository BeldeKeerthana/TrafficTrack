def number(
    payload,
    key,
    minimum=None,
    maximum=None
):

    try:

        value = float(
            payload.get(key)
        )

    except (
        TypeError,
        ValueError
    ):

        raise ValueError(
            f"{key} must be a number."
        )


    if (
        minimum is not None
        and value < minimum
    ):

        raise ValueError(
            f"{key} must be at least {minimum}."
        )


    if (
        maximum is not None
        and value > maximum
    ):

        raise ValueError(
            f"{key} must not exceed {maximum}."
        )


    return value


def validate_input(payload):

    road = str(
        payload.get(
            "road",
            ""
        )
    ).strip()


    if not road:

        raise ValueError(
            "Road name is required."
        )


    return {

        "road":
            road[:100],

        "lat":
            number(
                payload,
                "lat",
                -90,
                90
            ),

        "lng":
            number(
                payload,
                "lng",
                -180,
                180
            ),

        "vehicles_per_min":
            number(
                payload,
                "vehicles_per_min",
                0,
                1000
            ),

        "avg_speed_kmph":
            number(
                payload,
                "avg_speed_kmph",
                1,
                150
            ),

        "occupancy":
            number(
                payload,
                "occupancy",
                0,
                100
            ),

        "incident":
            int(
                bool(
                    payload.get(
                        "incident",
                        False
                    )
                )
            ),

        "roadwork":
            int(
                bool(
                    payload.get(
                        "roadwork",
                        False
                    )
                )
            ),

        "signal_delay_sec":
            number(
                payload,
                "signal_delay_sec",
                0,
                300
            ),

        "weather":
            number(
                payload,
                "weather",
                0,
                1
            )
    }