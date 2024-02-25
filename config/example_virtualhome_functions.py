# Functions to intereact with the VirtualHome environment
# House Assistants will have access to these functions

def retrieve_item(item, location_of_item, location_to_bring_item_to):
    """
    Retrieve an item from a location in the house
    :param item: The item to retrieve
    :param location: The location to retrieve the item from
    :return: The item retrieved
    """
    print(f"Retrieving {item} from {location_of_item} and bringing it to {location_to_bring_item_to}")
    
def open_fridge():
    """
    Open the fridge
    """
    print("Opening the fridge")

def close_fridge():
    """
    Close the fridge
    """
    print("Closing the fridge")

def turn_light_on(location):
    """
    Turn on the light in a room
    :param location: The room to turn the light on in
    """
    print(f"Turning on the light in the {location}")

def turn_light_off(location):
    """
    Turn off the light in a room
    :param location: The room to turn the light off in
    """
    print(f"Turning off the light in the {location}")

def water_plants(location):
    """
    Water the plants in a room
    :param location: The room where the plants are located
    """
    print(f"Watering the plants in the {location}")

def play_music(song):
    """
    Play music
    :param song: The song to play
    """
    print(f"Playing {song}")

def clean_room(location):
    """
    Clean a room
    :param location: The room to clean
    """
    print(f"Cleaning the {location}")

def feed_pet(pet, food):
    """
    Feed a pet
    :param pet: The pet to feed
    :param food: The food to feed the pet
    """
    print(f"Feeding {pet} with {food}")

def turn_on_tv():
    """
    Turn on the TV
    """
    print("Turning on the TV")

def turn_off_tv():
    """
    Turn off the TV
    """
    print("Turning off the TV")

def change_temperature(temperature):
    """
    Change the temperature to a specified value
    :param temperature: The desired temperature
    """
    print(f"Changing the temperature to {temperature}")