import anthropic
from opensky_tools import find_by_callsign, find_in_bounding_box

client = anthropic.Anthropic()

tools = [
    {
        "name": "find_by_callsign",
        "description": "Find a specific aircraft currently airborne by its flight callsign (e.g. KLM643).",
        "input_schema": {
            "type": "object",
            "properties": {
                "callsign": {"type": "string",
                             "description": "The flight callsign to search for"}
            },
            "required": ["callsign"]
        }
    },
    {
        "name": "find_in_bounding_box",
        "description": "Find all aircraft currently within a geographic bounding box, given min/max latitude and longitude.",
        "input_schema": {
            "type": "object",
            "properties": {
                "lat_min": {"type": "number"},
                "lat_max": {"type": "number"},
                "lon_min": {"type": "number"},
                "lon_max": {"type": "number"}
            },
            "required": ["lat_min", "lat_max",
                         "lon_min", "lon_max"]
        }
    }
]


def run_tool(name, tool_input):
    if name == "find_by_callsign":
        return find_by_callsign(tool_input["callsign"])
    
    elif name == "find_in_bounding_box":
        return find_in_bounding_box(
            tool_input["lat_min"], tool_input["lat_max"],
            tool_input["lon_min"], tool_input["lon_max"]
        )
        

def chat():
    print("Flight Tracker Agent. Ask about live flights (type 'quit' to exit).\n")
    
    messages = []

    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ("quit", "exit"):
            break

        messages.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        # Keep responding as long as Claude wants to use a tool
        while response.stop_reason == "tool_use":
            messages.append({"role":    "assistant",
                             "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = run_tool(block.name, block.input)
                    tool_results.append({
                        "type":        "tool_result",
                        "tool_use_id": block.id,
                        "content":     str(result)
                    })

            messages.append({"role":    "user",
                             "content": tool_results})

            response = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=1024,
                tools=tools,
                messages=messages
            )

        # Print the final text response
        for block in response.content:
            if block.type == "text":
                print(f"\nAgent: {block.text}\n")

        messages.append({"role":    "assistant",
                         "content": response.content})


if __name__ == "__main__":
    chat()