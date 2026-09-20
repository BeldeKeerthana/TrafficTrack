from datetime import datetime


class TrafficMemory:

    def __init__(self, rows):

        self.rows = rows


    def make_current_snapshot(self, data):

        now = datetime.now()

        return {

            "timestamp":
                now.isoformat(
                    timespec="seconds"
                ),

            "road":
                data["road"],

            "lat":
                data["lat"],

            "lng":
                data["lng"],

            "vehicles_per_min":
                data["vehicles_per_min"],

            "avg_speed_kmph":
                data["avg_speed_kmph"],

            "occupancy":
                data["occupancy"],

            "incident":
                data["incident"],

            "roadwork":
                data["roadwork"],

            "signal_delay_sec":
                data["signal_delay_sec"],

            "weather":
                data["weather"]
        }


    def similar_pattern(
        self,
        current,
        limit=5
    ):

        def distance(row):

            values = [

                abs(
                    row["vehicles_per_min"]
                    -
                    current["vehicles_per_min"]
                )
                /
                max(
                    1,
                    current["vehicles_per_min"]
                ),

                abs(
                    row["avg_speed_kmph"]
                    -
                    current["avg_speed_kmph"]
                )
                /
                max(
                    1,
                    current["avg_speed_kmph"]
                ),

                abs(
                    row["occupancy"]
                    -
                    current["occupancy"]
                )
                / 100,

                abs(
                    row["incident"]
                    -
                    current["incident"]
                ),

                abs(
                    row["roadwork"]
                    -
                    current["roadwork"]
                )
            ]

            return sum(values)


        matches = sorted(
            self.rows,
            key=distance
        )[:limit]


        result = []

        for row in matches:

            similarity = max(

                0,

                100
                *
                (
                    1
                    -
                    distance(row)
                    / 5
                )

            )

            result.append({

                "timestamp":
                    row["timestamp"],

                "road":
                    row["road"],

                "similarity":
                    round(
                        similarity,
                        1
                    ),

                "speed":
                    row["avg_speed_kmph"],

                "occupancy":
                    row["occupancy"]
            })

        return result