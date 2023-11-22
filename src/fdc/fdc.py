import json
from datatypes import Food, AbridgedFood
import requests
import humps


class FDC:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.nal.usda.gov/fdc/v1/"

    def get_food(self, id, _format="full", _nutrients=None):
        """
        Retrieves a single food item by an FDC ID. Optional format and nutrients can be specified.
        :param id: FDC id
        of the food to retrieve
        :param _format: Optional. 'abridged' for an abridged set of elements, 'full' for all
        elements (default).
        :param _nutrients: Optional. List of up to 25 nutrient numbers. Only the nutrient
        information for the specified nutrients will be returned. Should be comma separated list (e.g. nutrients=203,
        204) or repeating parameters (e.g. nutrients=203&nutrients=204). If a food does not have any matching
        nutrients, the food will be returned with an empty foodNutrients element.
        :return: Food or AbridgedFood object
        """

        url = self.base_url + f"food/{str(id)}?api_key={self.api_key}&format={_format}"
        if _nutrients:
            url += "&nutrients={_nutrients}"
        req = requests.get(url)
        if req.status_code == 200:
            result_json = humps.decamelize(json.loads(req.text))
            food = Food.Food(**result_json) if _format == "full" else AbridgedFood.AbridgedFood(**result_json)
            return food
        req.raise_for_status()

    def get_foods(self, ids, _format, _nutrients):
        url = self.base_url + f"foods/{str(id)}?api_key={self.api_key}&format={_format}&nutrients={_nutrients}"


if __name__ == "__main__":
    with open("../../config.json", "r") as file:
        json_file = json.load(file)
        key = json_file["api_key"]
    fdc = FDC(key)
    x = fdc.get_food(2262074, "abridged")
    print(x)
