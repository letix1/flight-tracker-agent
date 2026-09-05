import requests

def get_all_states():
    response = requests.get("https://opensky-network.org/api/states/all")
    response.raise_for_status()
    
    return response.json()


if __name__ == "__main__":
    data = get_all_states()
    print(f"Tracking {len(data['states'])} aircraft right now...")
    print(data["states"][0])  # look at one raw state vector