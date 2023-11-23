import json
from datatypes import Food, AbridgedFood
import requests
import humps
from typing import List


class FDC:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.nal.usda.gov/fdc/v1/"

    def get_food(self, id: str, _format: str = "full",
                 _nutrients: List[int] = None) -> Food.Food | AbridgedFood.AbridgedFood:
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
            url += f"&nutrients={_nutrients}"
        req = requests.get(url)
        if req.status_code == 200:
            result_json = humps.decamelize(json.loads(req.text))
            food = Food.Food(**result_json) if _format == "full" else AbridgedFood.AbridgedFood(**result_json)
            return food
        req.raise_for_status()

    def get_foods(self, ids: List[str], _format: str = "full",
                  _nutrients: List[int] = None) -> List[Food.Food] | List[AbridgedFood.AbridgedFood]:
        """
        Retrieves a list of food items by a list of up to 20 FDC IDs. Optional format and nutrients can be specified.
        Invalid FDC ID's or ones that are not found are omitted and an empty set is returned if there are no matches.
        :param ids: List of multiple FDC ID's
        :param _format: Optional. 'abridged' for an abridged set of elements, 'full' for all elements (default).
        :param _nutrients: Optional. List of up to 25 nutrient numbers. Only the nutrient
        information for the specified nutrients will be returned. Should be comma separated list (e.g. nutrients=203,
        204) or repeating parameters (e.g. nutrients=203&nutrients=204). If a food does not have any matching
        nutrients, the food will be returned with an empty foodNutrients element.
        :return: List of Food or AbridgedFood objects
        """
        url = self.base_url + f"foods?api_key={self.api_key}&format={_format}"
        for fdc_id in ids:
            url+=f"&fdcIds={fdc_id}"
        if _nutrients:
            url += f"&nutrients={_nutrients}"
        req = requests.get(url)
        if req.status_code == 200:
            result_json = humps.decamelize(json.loads(req.text))
            foods = [Food.Food(**item) for item in result_json] if _format == "full" else [AbridgedFood.AbridgedFood(**item) for item in result_json]
            return foods
        req.raise_for_status()


if __name__ == "__main__":
    with open("../../config.json", "r") as file:
        json_file = json.load(file)
        key = json_file["api_key"]
    fdc = FDC(key)
    x = fdc.get_foods(["2262074", "2262075"], "abridged")
    print(x)
