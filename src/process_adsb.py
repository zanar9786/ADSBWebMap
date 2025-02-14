def process_adsb_data(raw_data):
    """
    Processes raw ADS-B JSON data and converts it into GeoJSON format.

    Parameters:
    - raw_data (dict): JSON response from the ADS-B API.

    Returns:
    - dict: GeoJSON FeatureCollection of aircraft data.
    """
    if not raw_data or "ac" not in raw_data:
        return {"type": "FeatureCollection", "features": []}  # Return empty collection if no data

    features = []

    for aircraft in raw_data["ac"]:
        if "lat" in aircraft and "lon" in aircraft:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [aircraft["lon"], aircraft["lat"]]
                },
                "properties": {
                    "hex": aircraft.get("hex", "N/A"),
                    "type": aircraft.get("type", "Unknown"),
                    "callsign": aircraft.get("flight", "Unknown").strip(),
                    "altitude": aircraft.get("alt_baro", 0),
                    "speed": aircraft.get("gs", 0),
                    "heading": aircraft.get("true_heading", 0),
                    "operator": aircraft.get("ownOp", "Unknown"),
                    "category": aircraft.get("category", "N/A"),
                    "signal_strength": aircraft.get("rssi", "N/A"),
                    "seen": aircraft.get("seen", 0)
                }
            }
            features.append(feature)

    return {"type": "FeatureCollection", "features": features}
