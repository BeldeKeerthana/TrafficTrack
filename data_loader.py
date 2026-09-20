import csv


def load_history(path):

    rows = []

    with open(path, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    return rows


def clean_records(rows):

    clean = []

    for row in rows:

        try:

            item = {

                "timestamp":
                    row["timestamp"],

                "road":
                    row["road"],

                "lat":
                    float(row["lat"]),

                "lng":
                    float(row["lng"]),

                "vehicles_per_min":
                    max(
                        0,
                        float(row["vehicles_per_min"])
                    ),

                "avg_speed_kmph":
                    max(
                        1,
                        float(row["avg_speed_kmph"])
                    ),

                "occupancy":
                    min(
                        100,
                        max(
                            0,
                            float(row["occupancy"])
                        )
                    ),

                "incident":
                    int(float(row.get("incident", 0))),

                "roadwork":
                    int(float(row.get("roadwork", 0))),

                "signal_delay_sec":
                    max(
                        0,
                        float(
                            row.get(
                                "signal_delay_sec",
                                0
                            )
                        )
                    ),

                "weather":
                    float(
                        row.get(
                            "weather",
                            0
                        )
                    )
            }

            clean.append(item)

        except (ValueError, KeyError):

            continue

    return clean