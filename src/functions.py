
import json

def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    print(f"Running get_current_weather({location})")

    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})
    
def move_to_object(object, action="walk"):
    """Move to an object in the scene"""
    print(f"Running move_to_object({action}, {object})")
    return json.dumps({"action": action, "object": object})