class TrafficGhost:

    def __init__(self, memory):

        self.memory = memory

    def detect(
        self,
        segment_id,
        timestamp,
        current_congestion
    ):

        historical = self.memory.lookup(
            segment_id,
            timestamp
        )

        historical_congestion = (
            historical[
                "historical_congestion"
            ]
        )

        standard_deviation = max(
            historical[
                "historical_std"
            ],
            0.02
        )

        difference = (
            float(current_congestion)
            - historical_congestion
        )

        if historical_congestion >= 0.60:

            status = (
                "recurring_congestion_pattern"
            )

        elif (
            difference >=
            1.5 * standard_deviation
            and
            float(current_congestion) >= 0.35
        ):

            status = (
                "early_warning_pattern"
            )

        else:

            status = (
                "normal_pattern"
            )

        return {
            "status": status,

            "historical_congestion": round(
                historical_congestion,
                4
            ),

            "current_congestion": round(
                float(current_congestion),
                4
            ),

            "difference_from_history": round(
                difference,
                4
            ),

            "history_count": historical[
                "history_count"
            ]
        }