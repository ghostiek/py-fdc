import json
from datatypes import AbridgedFood, FoundationFood, MarketAcquisitionFood, SampleFood, BrandedFood, SRLegacyFood, SurveyFood, Food
import requests
import humps
from typing import List


class FDC:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.nal.usda.gov/fdc/v1/"

    def get_food(self, id: str, _format: str = "full",
                 _nutrients: List[int] = None, raw: bool = False) \
            -> str | Food.Food:
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
        :param raw: Optional. Return the raw json string if True, else serialize the output
        :return: Food object
        """

        url = self.base_url + f"food/{str(id)}?api_key={self.api_key}&format={_format}"
        if _nutrients:
            url += f"&nutrients={_nutrients}"
        req = requests.get(url)
        if req.status_code != 200:
            req.raise_for_status()

        item = humps.decamelize(json.loads(req.text))
        if raw:
            return req.text
        food = self._match_data_type(item, _format)
        return food

    def get_foods(self, ids: List[str], _format: str = "full", _nutrients: List[int] = None, raw: bool = False) \
            -> str | List[Food.Food]:
        """
        Retrieves a list of food items by a list of up to 20 FDC IDs. Optional format and nutrients can be specified.
        Invalid FDC ID's or ones that are not found are omitted and an empty set is returned if there are no matches.
        :param ids: List of multiple FDC ID's
        :param _format: Optional. 'abridged' for an abridged set of elements, 'full' for all elements (default).
        :param _nutrients: Optional. List of up to 25 nutrient numbers. Only the nutrient
        information for the specified nutrients will be returned. Should be comma separated list (e.g. nutrients=203,
        204) or repeating parameters (e.g. nutrients=203&nutrients=204). If a food does not have any matching
        nutrients, the food will be returned with an empty foodNutrients element.
        :param raw: Optional. Return the raw json string if True, else serialize the output
        :return: List of Food Objects
        """
        url = self.base_url + f"foods?api_key={self.api_key}&format={_format}"
        for fdc_id in ids:
            url += f"&fdcIds={fdc_id}"
        if _nutrients:
            url += f"&nutrients={_nutrients}"
        req = requests.get(url)
        if req.status_code != 200:
            req.raise_for_status()

        result_json = humps.decamelize(json.loads(req.text))
        if raw:
            return req.text
        foods = []
        for item in result_json:
            food = self._match_data_type(item, _format)
            foods.append(food)

        return foods

    def _match_data_type(self, item: dict, _format: str) -> Food.Food:
        """
        Used to serialize the FoodItem properly.
        :param item: JSON of the food item.
        :param _format: Was the query Full or Abridged
        :return: A `Food` class
        """
        food = None
        if _format == "abridged":
            food = AbridgedFood.AbridgedFood(**item)
        elif item["data_type"] == "Branded":
            food = BrandedFood.BrandedFood(**item)
        elif item["data_type"] == "Foundation":
            food = FoundationFood.FoundationFood(**item)
        elif item["data_type"] == "SR Legacy":
            food = SRLegacyFood.SRLegacyFood(**item)
        elif item["data_type"] == "Survey (FNDDS)":
            food = SurveyFood.SurveyFood(**item)
        elif item["data_type"] == "Market Acquisition":
            food = MarketAcquisitionFood.MarketAcquisitionFood(**item)
        elif item["data_type"] == "Sample":
            food = SampleFood.SampleFood(**item)
        else:
            print(f"Unexpected DataType: {item['data_type']}")
        return food


if __name__ == "__main__":
    with open("../../config.json", "r") as file:
        json_file = json.load(file)
        key = json_file["api_key"]
    fdc = FDC(key)
    for i in range(100):
        x = fdc.get_food(str(2262077 + i))
    #x = fdc.get_foods(["2262077", "2262077"], "full")
    print(x)
