import json
from datatypes import Food
import requests
import humps


class FDC:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.nal.usda.gov/fdc/v1/"

    def get_food(self, id):
        url = self.base_url + f"food/{str(id)}?api_key={self.api_key}"
        req = requests.get(url)
        if req.status_code == 200:
            result_json = humps.decamelize(json.loads(req.text))
            food = Food.Food(**result_json)
            return food
        req.raise_for_status()



if __name__ == "__main__":
    with open("../../config.json", "r") as file:
        json_file = json.load(file)
        key = json_file["api_key"]
    fdc = FDC(key)
    x = fdc.get_food(1)
    print(x)