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

if __name__ == "__main__":
    results = find_by_callsign("KLM643")
    if results:
        for r in results:
            print(f"Found: {r[1].strip()}, altitude: {r[7]}m, speed: {r[9]}m/s, over ({r[6]}, {r[5]})")
    else:
        print("No matching flight currently airborne with that callsign.")
