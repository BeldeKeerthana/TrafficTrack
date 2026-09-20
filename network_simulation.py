import pandas as pd


class NetworkSimulator:

    def __init__(self, network):

        self.network = network.copy()

        numeric_columns = [
            "lanes",
            "capacity_vph",
            "length_km",
            "importance",
            "peak_capacity_factor",
            "structural_bottleneck"
        ]

        for column in numeric_columns:

            if column in self.network.columns:

                self.network[column] = (
                    pd.to_numeric(
                        self.network[column],
                        errors="coerce"
                    )
                    .fillna(0)
                )

    def segment_effect(
        self,
        segment_id,
        current_flow,
        current_congestion,
        diversion=0,
        capacity_delta=0
    ):

        rows = self.network[
            self.network["segment_id"]
            == segment_id
        ]

        if rows.empty:

            return {
                "segment_id": segment_id,
                "capacity": 0,
                "flow": float(current_flow),
                "congestion": float(
                    current_congestion
                )
            }

        row = rows.iloc[0]

        base_capacity = float(
            row["capacity_vph"]
        )

        capacity = (
            base_capacity
            + float(capacity_delta)
        )

        capacity = max(
            1,
            capacity
        )

        diversion = max(
            0,
            min(
                100,
                float(diversion)
            )
        )

        flow = (
            float(current_flow)
            * (1 - diversion / 100)
        )

        flow = max(
            0,
            flow
        )

        demand_ratio = (
            flow / capacity
        )

        bottleneck_factor = 1.0

        if (
            "structural_bottleneck"
            in row
            and
            float(
                row["structural_bottleneck"]
            ) > 0
        ):

            bottleneck_factor = 1.12

        congestion = (
            0.55 *
            demand_ratio *
            bottleneck_factor
            +
            0.45 *
            float(current_congestion)
            *
            (1 - diversion / 100)
        )

        congestion = max(
            0,
            min(
                1,
                congestion
            )
        )

        return {
            "segment_id": segment_id,
            "capacity": round(
                capacity,
                2
            ),
            "flow": round(
                flow,
                2
            ),
            "congestion": round(
                congestion,
                4
            )
        }