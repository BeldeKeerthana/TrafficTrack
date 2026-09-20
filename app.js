let map;

let marker;

let circle;

let latestData = null;


// --------------------------------
// GOOGLE MAP
// --------------------------------

function initMap() {

    const center = {

        lat: 17.4435,

        lng: 78.3772
    };


    if (
        !window.google ||
        !google.maps
    ) {

        document.getElementById(
            "map"
        ).innerHTML =

            "<div style='padding:30px;color:#ff9d9d'>" +

            "Google Maps could not load. " +

            "Check your API key, billing, " +

            "Maps JavaScript API and restrictions." +

            "</div>";

        return;
    }


    map = new google.maps.Map(

        document.getElementById(
            "map"
        ),

        {

            center: center,

            zoom: 12,

            mapTypeControl: true,

            streetViewControl: false
        }
    );


    marker =
        new google.maps.Marker({

            map: map,

            position: center,

            title:
                "Traffic monitoring point"
        });
}


// --------------------------------
// GET VALUE
// --------------------------------

function value(id) {

    return document
        .getElementById(id)
        .value;
}


// --------------------------------
// CHECKBOX
// --------------------------------

function isChecked(id) {

    return document
        .getElementById(id)
        .checked;
}


// --------------------------------
// DISPLAY ANALYSIS
// --------------------------------

function renderAnalysis(data) {

    latestData = data;


    document.getElementById(
        "currentRisk"
    ).textContent =
        data.forecast.current_score;


    document.getElementById(
        "peakRisk"
    ).textContent =
        data.forecast.peak_score;


    document.getElementById(
        "peakTime"
    ).textContent =
        data.forecast.peak_minutes
        + " min";


    document.getElementById(
        "modelRows"
    ).textContent =
        data.model.trained_rows;


    document.getElementById(
        "locationText"
    ).textContent =

        data.current.lat.toFixed(5)
        +
        ", "
        +
        data.current.lng.toFixed(5);


    document.getElementById(
        "severityText"
    ).textContent =
        data.forecast.risk;


    // -----------------------------
    // FORECAST
    // -----------------------------

    const forecast =
        document.getElementById(
            "forecast"
        );


    forecast.innerHTML =

        data.forecast.points

        .map(point => `

            <div class="forecastCard">

                <span>
                    ${point.minutes} minutes
                </span>

                <strong class="${point.level}">
                    ${point.risk_score}
                </strong>

                <small>
                    ${point.level} risk
                </small>

            </div>

        `)

        .join("");



    // -----------------------------
    // TRAFFIC GHOST
    // -----------------------------

    const ghost =
        document.getElementById(
            "ghost"
        );


    ghost.innerHTML =

        data.ghost

        .map(item => `

            <div
                class="forecastCard"
                style="margin:8px 0"
            >

                <b>
                    ${item.road}
                </b>

                <br>

                ${item.timestamp}

                <br>

                Similarity:
                ${item.similarity}%

                · Speed:
                ${item.speed}
                km/h

                · Occupancy:
                ${item.occupancy}%

            </div>

        `)

        .join("");



    // -----------------------------
    // WHAT IF
    // -----------------------------

    const scenarios =
        document.getElementById(
            "scenarios"
        );


    scenarios.innerHTML =

        data.scenarios

        .map(item => `

            <div class="scenario">

                <span>

                    ${item.diversion_percent}%
                    diversion

                </span>

                <strong>

                    ${item.projected_congestion}

                </strong>

                <small>

                    Projected congestion

                    <br>

                    Vehicles diverted/min:
                    ${item.vehicles_diverted_per_min}

                    <br>

                    Estimated travel:
                    ${item.estimated_travel_minutes}
                    min

                    <br>

                    ${item.status}

                </small>

            </div>

        `)

        .join("");



    // -----------------------------
    // POLICE ALERT
    // -----------------------------

    const risk =
        data.forecast.risk;


    if (risk === "LOW") {

        document.getElementById(
            "alertText"
        ).textContent =
            "No immediate high-risk alert.";

    } else {

        document.getElementById(
            "alertText"
        ).textContent =

            "Potential congestion on "
            +
            data.current.road
            +
            " within "
            +
            data.forecast.peak_minutes
            +
            " minutes.";
    }


    if (risk === "LOW") {

        document.getElementById(
            "actionText"
        ).textContent =
            "Continue monitoring.";

    } else {

        document.getElementById(
            "actionText"
        ).textContent =

            "Review simulated diversion scenarios and make the operational decision manually.";
    }



    // -----------------------------
    // PUBLIC ADVISORY
    // -----------------------------

    document.getElementById(
        "advisory"
    ).textContent =

        "Traffic advisory: "
        +
        data.current.road
        +
        " may experience "
        +
        risk.toLowerCase()
        +
        " congestion risk over the next "
        +
        data.forecast.peak_minutes
        +
        " minutes. Drivers should check live navigation conditions and consider alternate routes where appropriate.";



    // -----------------------------
    // MOVE MAP
    // -----------------------------

    if (map) {

        const position = {

            lat:
                data.current.lat,

            lng:
                data.current.lng
        };


        map.setCenter(
            position
        );


        map.setZoom(14);


        marker.setPosition(
            position
        );


        if (circle) {

            circle.setMap(null);
        }


        circle =
            new google.maps.Circle({

                map: map,

                center: position,

                radius: 500,

                strokeOpacity: 0.7,

                fillOpacity: 0.18
            });
    }
}


// --------------------------------
// TRAFFIC FORM
// --------------------------------

document
    .getElementById(
        "trafficForm"
    )
    .addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const payload = {

                road:
                    value("road"),

                lat:
                    Number(
                        value("lat")
                    ),

                lng:
                    Number(
                        value("lng")
                    ),

                vehicles_per_min:
                    Number(
                        value(
                            "vehicles_per_min"
                        )
                    ),

                avg_speed_kmph:
                    Number(
                        value(
                            "avg_speed_kmph"
                        )
                    ),

                occupancy:
                    Number(
                        value("occupancy")
                    ),

                signal_delay_sec:
                    Number(
                        value(
                            "signal_delay_sec"
                        )
                    ),

                weather:
                    Number(
                        value("weather")
                    ),

                incident:
                    isChecked(
                        "incident"
                    ),

                roadwork:
                    isChecked(
                        "roadwork"
                    )
            };


            const response =
                await fetch(
                    "/api/analyze",
                    {

                        method:
                            "POST",

                        headers: {

                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                payload
                            )
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                alert(
                    data.error
                    ||
                    "Traffic analysis failed."
                );

                return;
            }


            renderAnalysis(
                data
            );
        }
    );


// --------------------------------
// GOOGLE ROUTES
// --------------------------------

document
    .getElementById(
        "routeBtn"
    )
    .addEventListener(
        "click",
        async function() {

            const origin =
                value("origin");

            const destination =
                value("destination");


            const result =
                document.getElementById(
                    "routeResult"
                );


            result.textContent =
                "Requesting Google Routes...";


            const response =
                await fetch(
                    "/api/route",
                    {

                        method:
                            "POST",

                        headers: {

                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({

                                origin:
                                    origin,

                                destination:
                                    destination
                            })
                    }
                );


            const data =
                await response.json();


            if (!data.ok) {

                result.textContent =
                    data.message
                    ||
                    "Google Routes request failed.";

                return;
            }


            result.innerHTML =

                data.routes

                .map(
                    function(route, index) {

                        const duration =
                            (
                                route.duration
                                ||
                                ""
                            ).replace(
                                "s",
                                " sec"
                            );


                        const distance =
                            route.distanceMeters

                            ?

                            (
                                route.distanceMeters
                                / 1000
                            ).toFixed(1)
                            +
                            " km"

                            :

                            "—";


                        return `

                            <div>

                                <b>
                                    Route ${index + 1}
                                </b>

                                :
                                ${distance}

                                ,
                                ${duration}

                                <br>

                                ${route.description || ""}

                            </div>

                            <hr>

                        `;
                    }
                )

                .join("");
        }
    );


// --------------------------------
// DIVERSION PLAN
// --------------------------------

document
    .getElementById(
        "divertBtn"
    )
    .addEventListener(
        "click",
        function() {

            if (!latestData) {

                alert(
                    "Run traffic analysis first."
                );

                return;
            }


            const scenarios =
                latestData.scenarios;


            const bestScenario =
                scenarios.reduce(
                    function(a, b) {

                        return
                            a.projected_congestion
                            <
                            b.projected_congestion

                            ?

                            a

                            :

                            b;
                    }
                );


            document.getElementById(
                "diversion"
            ).innerHTML = `

                <div class="advisory">

                    <b>
                        Draft Diversion Plan
                    </b>

                    <br><br>

                    Simulated diversion:
                    ${bestScenario.diversion_percent}%

                    <br>

                    Projected congestion:
                    ${bestScenario.projected_congestion}

                    <br>

                    Vehicles diverted/min:
                    ${bestScenario.vehicles_diverted_per_min}

                    <br><br>

                    <b>
                        Manual police approval is required
                        before implementation.
                    </b>

                </div>
            `;
        }
    );