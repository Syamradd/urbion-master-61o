
# ============================================================
# 🗺️ URBION SPATIAL INTELLIGENCE
# ============================================================

def urbion_create_spatial_context(
    precinct=None,
    precinct_verified=False,
    tod_verified=False,
    tod_400_verified=False,
    tod_800_verified=False,
    shop_frontage_verified=False,
    shop_office_verified=False,
    tod_distance_m=None
):
    """
    Create a controlled spatial context object.

    URBION does not infer spatial verification
    without supporting evidence.
    """

    return {

        "precinct":
            precinct,

        "precinct_verified":
            bool(
                precinct_verified
            ),

        "tod_verified":
            bool(
                tod_verified
            ),

        "tod_400_verified":
            bool(
                tod_400_verified
            ),

        "tod_800_verified":
            bool(
                tod_800_verified
            ),

        "shop_frontage_verified":
            bool(
                shop_frontage_verified
            ),

        "shop_office_verified":
            bool(
                shop_office_verified
            ),

        "tod_distance_m":
            tod_distance_m
    }


def urbion_get_spatial_status(
    spatial_context
):
    """
    Convert spatial verification fields
    into human-readable statuses.
    """

    context = (
        spatial_context
        or {}
    )

    return {

        "Precinct":
            (
                "🟢 VERIFIED"
                if context.get(
                    "precinct_verified",
                    False
                )
                else
                "🟡 NOT VERIFIED"
            ),

        "TOD 400m":
            (
                "🟢 VERIFIED"
                if context.get(
                    "tod_400_verified",
                    False
                )
                else
                "🟡 NOT VERIFIED"
            ),

        "TOD 800m":
            (
                "🟢 VERIFIED"
                if context.get(
                    "tod_800_verified",
                    False
                )
                else
                "🟡 NOT VERIFIED"
            ),

        "Shop Frontage":
            (
                "🟢 VERIFIED"
                if context.get(
                    "shop_frontage_verified",
                    False
                )
                else
                "🟡 NOT VERIFIED"
            )
    }


def urbion_spatial_verification_summary(
    spatial_context
):
    """
    Produce an evidence-aware spatial summary.

    No spatial condition is claimed as verified
    unless the corresponding verification flag
    is explicitly true.
    """

    context = (
        spatial_context
        or {}
    )

    statuses = (
        urbion_get_spatial_status(
            context
        )
    )

    verified_count = sum(
        1
        for value in statuses.values()
        if "VERIFIED" in value
        and "NOT VERIFIED" not in value
    )

    total_count = len(
        statuses
    )

    return {

        "statuses":
            statuses,

        "verified_count":
            verified_count,

        "total_checks":
            total_count,

        "verification_state":
            (
                "🟢 VERIFIED"
                if verified_count == total_count
                else
                "🟡 PARTIALLY VERIFIED"
                if verified_count > 0
                else
                "🟡 NOT VERIFIED"
            )
    }


# ============================================================
# 🗺️ GIS DISTANCE ENGINE
# ============================================================

def calculate_distance_m(
    lat1,
    lon1,
    lat2,
    lon2
):
    """
    Calculate approximate straight-line distance
    between two geographic coordinates in metres.
    """

    import math

    R = 6371000

    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))

    d_phi = math.radians(
        float(lat2) - float(lat1)
    )

    d_lambda = math.radians(
        float(lon2) - float(lon1)
    )

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(d_lambda / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


def classify_tod_distance(
    distance_m
):
    """
    Classify a verified straight-line distance
    against URBION TOD thresholds.
    """

    if distance_m is None:
        return "NO TOD DISTANCE"

    distance_m = float(distance_m)

    if distance_m <= 400:
        return "TOD 400m"

    if distance_m <= 800:
        return "TOD 800m"

    return "OUTSIDE TOD 800m"
