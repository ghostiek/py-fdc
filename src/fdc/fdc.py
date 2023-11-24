import json
from datatypes import Food, AbridgedFood, FoundationFood, MarketAcquisitionFood
import requests
import humps
from typing import List


class FDC:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.nal.usda.gov/fdc/v1/"

    def get_food(self, id: str, _format: str = "full",
                 _nutrients: List[int] = None, raw: bool = False) \
            -> str | FoundationFood.FoundationFood | AbridgedFood.AbridgedFood | \
               MarketAcquisitionFood.MarketAcquisitionFood:
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
        :return: Food or AbridgedFood object
        """

        url = self.base_url + f"food/{str(id)}?api_key={self.api_key}&format={_format}"
        if _nutrients:
            url += f"&nutrients={_nutrients}"
        req = requests.get(url)
        if req.status_code != 200:
            req.raise_for_status()

        result_json = humps.decamelize(json.loads(req.text))
        food = None
        if raw:
            return req.text
        elif _format == "abridged":
            food = AbridgedFood.AbridgedFood(**result_json)
        elif result_json["data_type"] == "Foundation":
            food = FoundationFood.FoundationFood(**result_json)
        elif result_json["data_type"] == "Branded":
            pass
        elif result_json["data_type"] == "Foundation":
            food = FoundationFood.FoundationFood(**result_json)
        elif result_json["data_type"] == "SR Legacy":
            pass
        elif result_json["data_type"] == "Survey (FNDDS)":
            pass
        elif result_json["data_type"] == "Market Acquisition":
            food = MarketAcquisitionFood.MarketAcquisitionFood(**result_json)
        else:
            print(f"Unexpected DataType: {result_json['data_type']}")
        return food

    def get_foods(self, ids: List[str], _format: str = "full", _nutrients: List[int] = None, raw: bool = False) \
            -> str | List[FoundationFood.FoundationFood] | List[AbridgedFood.AbridgedFood] | \
               List[MarketAcquisitionFood.MarketAcquisitionFood]:
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
        :return: List of FoundationFood, AbridgedFood, SRLegacyFood, BrandedFood, or SurveryFood objects
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
            if _format == "abridged":
                foods.append(AbridgedFood.AbridgedFood(**result_json))
            elif item["data_type"] == "Branded":
                pass
            elif item["data_type"] == "Foundation":
                foods.append(FoundationFood.FoundationFood(**item))
            elif item["data_type"] == "SR Legacy":
                pass
            elif item["data_type"] == "Survey (FNDDS)":
                pass
            elif item["data_type"] == "Market Acquisition":
                foods.append(MarketAcquisitionFood.MarketAcquisitionFood(**item))
            else:
                print(f"Unexpected DataType: {item['data_type']}")
                foods.append(None)
        return foods


if __name__ == "__main__":
    with open("../../config.json", "r") as file:
        json_file = json.load(file)
        key = json_file["api_key"]
    fdc = FDC(key)
    x = fdc.get_foods(["2262075", "2262076"], "full")
    print(x)
