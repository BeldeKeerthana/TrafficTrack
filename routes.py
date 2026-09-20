import json
import urllib.request
import urllib.error


def google_route(
    origin,
    destination,
    api_key
):

    if not api_key:

        return {

            "ok": False,

            "message":
                "Google Maps API key is not configured. "
                "Add GOOGLE_MAPS_API_KEY to .env."
        }


    url = (
        "https://routes.googleapis.com/"
        "directions/v2:computeRoutes"
    )


    body = {

        "origin": {

            "address":
                origin
        },

        "destination": {

            "address":
                destination
        },

        "travelMode":
            "DRIVE",

        "routingPreference":
            "TRAFFIC_AWARE",

        "computeAlternativeRoutes":
            True,

        "languageCode":
            "en-US",

        "units":
            "METRIC"
    }


    request_data = json.dumps(
        body
    ).encode("utf-8")


    request = urllib.request.Request(

        url,

        data=request_data,

        method="POST",

        headers={

            "Content-Type":
                "application/json",

            "X-Goog-Api-Key":
                api_key,

            "X-Goog-FieldMask":
                (
                    "routes.duration,"
                    "routes.distanceMeters,"
                    "routes.description,"
                    "routes.polyline.encodedPolyline"
                )
        }
    )


    try:

        with urllib.request.urlopen(
            request,
            timeout=20
        ) as response:

            result = json.loads(
                response
                .read()
                .decode("utf-8")
            )


        return {

            "ok": True,

            "routes":
                result.get(
                    "routes",
                    []
                )
        }


    except urllib.error.HTTPError as error:

        detail = (
            error
            .read()
            .decode(
                "utf-8",
                errors="replace"
            )
        )

        return {

            "ok": False,

            "message":
                f"Google Routes API error {error.code}",

            "detail":
                detail
        }


    except Exception as error:

        return {

            "ok": False,

            "message":
                str(error)
        }