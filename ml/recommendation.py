def calculate_score(station):

    distance = station["distance"]

    brand = station["properties"].get("brand", "")

    # -------------------------
    # Distance Score (40)
    # -------------------------

    if distance <= 1:
        distance_score = 40

    elif distance <= 2:
        distance_score = 35

    elif distance <= 3:
        distance_score = 30

    elif distance <= 5:
        distance_score = 20

    else:
        distance_score = 10

    # -------------------------
    # Brand Score (30)
    # -------------------------

    brand_scores = {

        "Indian Oil":30,

        "Hindustan Petroleum":28,

        "HP":28,

        "Bharat Petroleum":27,

        "Reliance":24,

        "Shell":23

    }

    brand_score = brand_scores.get(brand,15)

    # -------------------------
    # Fuel Type Score (20)
    # -------------------------

    fuel_score = 20

    # -------------------------
    # Rating Score (10)
    # -------------------------

    rating_score = 8

    station["ai_score"] = (

        distance_score +

        brand_score +

        fuel_score +

        rating_score

    )

    return station