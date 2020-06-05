import json

definitions_path = '/Users/Famosi/Desktop/SocialRobot-ISL/definitions/'

# Get angles from Json
def get_angles(path, element):
    f = open(path)
    data = json.load(f)
    if data[element] is not None:
        return data[element]
    return None
