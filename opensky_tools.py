import requests

def get_all_states():
    response = requests.get("https://opensky-network.org/api/states/all")
    response.raise_for_status()
    
    return response.json()["states"]


def find_by_callsign(callsign):
    states = get_all_states()
    callsign = callsign.strip().upper()
    matches = [s for s in states if s[1] and s[1].strip().upper() == callsign]
    
    return matches


def find_in_bounding_box(lat_min, lat_max, lon_min, lon_max):
    states = get_all_states()
    
    matches = [
        s for s in states
        if s[6] is not None and s[5] is not None
        and lat_min <= s[6] <= lat_max
        and lon_min <= s[5] <= lon_max
    ]
    
    return matches


if __name__ == "__main__":
    results = find_by_callsign("KLM643")
    
    if results:
        for r in results:
            print(f"Found: {r[1].strip()}, altitude: {r[7]}m, speed: {r[9]}m/s, over ({r[6]}, {r[5]})")
    
    else:
        print("No matching flight currently airborne with that callsign.")

    nl_flights = find_in_bounding_box(50.75, 53.7, 3.3, 7.2)
    
    print(f"\n{len(nl_flights)} aircraft currently over the Netherlands")
    
    for f in nl_flights[:5]:
        altitude = f"{f[7]}m" if f[7] is not None else "unknown"
        
        print(f"  {f[1].strip() if f[1] else 'unknown'}: altitude {altitude}")