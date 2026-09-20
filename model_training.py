import math
from datetime import datetime


def create_features(row):

    timestamp = datetime.fromisoformat(
        row["timestamp"]
    )

    return [

        row["vehicles_per_min"],

        row["avg_speed_kmph"],

        row["occupancy"],

        row["incident"],

        row["roadwork"],

        row["signal_delay_sec"],

        row["weather"],

        timestamp.hour
        + timestamp.minute / 60,

        timestamp.weekday()
    ]


def calculate_congestion(row):

    speed_component = max(
        0,
        min(
            100,
            100 - row["avg_speed_kmph"] * 2.2
        )
    )

    volume_component = max(
        0,
        min(
            100,
            row["vehicles_per_min"] * 2
        )
    )

    occupancy_component = row["occupancy"]

    context = (

        row["incident"] * 18

        +

        row["roadwork"] * 10

        +

        min(
            20,
            row["signal_delay_sec"] / 3
        )

    )

    score = (

        0.30 * speed_component

        +

        0.25 * volume_component

        +

        0.30 * occupancy_component

        +

        0.15 * min(
            100,
            context
        )

    )

    return max(
        0,
        min(
            100,
            score
        )
    )


class TrafficModel:

    name = "Traffic Memory Forecast Model"

    def __init__(self):

        self.ready = False

        self.mean = []

        self.std = []

        self.weights = []

        self.bias = 0


    def fit(self, rows):

        if not rows:

            raise ValueError(
                "Training dataset is empty."
            )

        X = [
            create_features(row)
            for row in rows
        ]

        Y = [
            calculate_congestion(row)
            for row in rows
        ]

        n = len(X)

        dimensions = len(X[0])

        self.mean = []

        self.std = []

        for j in range(dimensions):

            average = sum(
                x[j]
                for x in X
            ) / n

            self.mean.append(
                average
            )

            variance = sum(
                (
                    x[j] - average
                ) ** 2
                for x in X
            ) / n

            deviation = math.sqrt(
                variance
            )

            self.std.append(
                deviation or 1
            )

        normalized = []

        for row in X:

            normalized.append([

                (
                    row[j]
                    - self.mean[j]
                )
                / self.std[j]

                for j in range(dimensions)

            ])

        self.weights = [
            0
            for _ in range(dimensions)
        ]

        self.bias = sum(Y) / n

        learning_rate = 0.035

        regularization = 0.004

        for _ in range(3500):

            weight_gradient = [
                0
                for _ in range(dimensions)
            ]

            bias_gradient = 0

            for x, target in zip(
                normalized,
                Y
            ):

                prediction = (

                    self.bias

                    +

                    sum(
                        a * b
                        for a, b
                        in zip(
                            self.weights,
                            x
                        )
                    )
                )

                error = (
                    prediction
                    -
                    target
                )

                bias_gradient += error

                for j in range(dimensions):

                    weight_gradient[j] += (
                        error * x[j]
                    )

            for j in range(dimensions):

                self.weights[j] -= (

                    learning_rate
                    *

                    (
                        2
                        * weight_gradient[j]
                        / n

                        +

                        regularization
                        * self.weights[j]
                    )
                )

            self.bias -= (

                learning_rate
                *

                (
                    2
                    * bias_gradient
                    / n
                )
            )

        self.ready = True


    def predict(self, row):

        if not self.ready:

            raise RuntimeError(
                "Model has not been trained."
            )

        values = create_features(
            row
        )

        normalized = [

            (
                values[j]
                -
                self.mean[j]
            )
            /
            self.std[j]

            for j in range(
                len(values)
            )
        ]

        prediction = (

            self.bias

            +

            sum(
                weight * value
                for weight, value
                in zip(
                    self.weights,
                    normalized
                )
            )
        )

        return max(
            0,
            min(
                100,
                prediction
            )
        )