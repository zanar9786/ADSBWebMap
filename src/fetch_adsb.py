import os
import requests

API_URL = "https://api.airplanes.live/v2/"

def request_adsb(filter_type="point", filter_value=None, lat=40.0, lon=-100.0, radius=250):
    """ 
    Fetches ADS-B data based on different filter options.  Returns JSON response if successful, otherwise 
    """

    # Construct API URL based on filter type
    if filter_type in ["hex", "callsign", "reg", "type", "squawk"]:
        if not filter_value:
            raise ValueError(f"{filter_type} request API requires a filter_value.")
        url = f"{API_URL}{filter_type}/{filter_value}"

    elif filter_type in ["mil", "ladd", "pia"]:
        url = f"{API_URL}{filter_type}"
    
    elif filter_type == "point":
        if radius > 250:
            print("Radius set to maximum (250m).")
        url = f"{API_URL}point/{lat}/{lon}/{min(radius, 250)}"  # Ensure max radius is 250
    
    else:
        raise ValueError(f"Invalid filter type: {filter_type}. Must be one of: hex, callsign, reg, type, squawk, mil, ladd, pia, point")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return response.json()
    
    except requests.RequestException as e:
        print(f"Error fetching ADS-B data: {e}")
        return None

def websocket_adsbdata(ulr):
    return