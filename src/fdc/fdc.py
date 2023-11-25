import json
from datatypes import AbridgedFood, FoundationFood, MarketAcquisitionFood, SampleFood, BrandedFood, SRLegacyFood, \
    SurveyFood, Food, ExperimentalFood, SearchResult
import requests
import humps
from typing import List


class FDC:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.nal.usda.gov/fdc/v1/"

    def get_food(self, id: str, _format: str = "full", _nutrients: List[int] = None) -> Food.Food:
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
        :return: `Food` object
        """
        req = self._call_food(id, _format, _nutrients)
        item = humps.decamelize(json.loads(req.text))
        food = self._match_data_type(item, _format)
        return food

    def get_food_raw(self, id: str, _format: str = "full", _nutrients: List[int] = None) -> str:
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
        :return: `str` of json
        """
        req = self._call_food(id, _format, _nutrients)
        return req.text

    def _call_food(self, id: str, _format: str = "full", _nutrients: List[int] = None) -> requests.Response:
        url = self.base_url + f"food/{str(id)}?api_key={self.api_key}&format={_format}"
        if _nutrients:
            url += f"&nutrients={_nutrients}"
        req = requests.get(url)
        if req.status_code != 200:
            req.raise_for_status()
        return req

    def get_foods(self, ids: List[str], format_: str = "full", _nutrients: List[int] = None) \
            -> List[Food.Food]:
        """
        Retrieves a list of food items by a list of up to 20 FDC IDs. Optional format and nutrients can be specified.
        Invalid FDC ID's or ones that are not found are omitted and an empty set is returned if there are no matches.
        :param ids: List of multiple FDC ID's
        :param format_: Optional. 'abridged' for an abridged set of elements, 'full' for all elements (default).
        :param nutrients: Optional. List of up to 25 nutrient numbers. Only the nutrient
        information for the specified nutrients will be returned. Should be comma separated list (e.g. nutrients=203,
        204) or repeating parameters (e.g. nutrients=203&nutrients=204). If a food does not have any matching
        nutrients, the food will be returned with an empty foodNutrients element.
        :return: List of `Food` Objects
        """
        req = self._call_foods(ids, format_, _nutrients)
        result_json = humps.decamelize(json.loads(req.text))
        foods = []
        for item in result_json:
            food = self._match_data_type(item, format_)
            foods.append(food)
        return foods

    def get_foods_raw(self, ids: List[str], format_: str = "full", nutrients: List[int] = None) -> str:
        """
        Retrieves a list of food items by a list of up to 20 FDC IDs. Optional format and nutrients can be specified.
        Invalid FDC ID's or ones that are not found are omitted and an empty set is returned if there are no matches.
        :param ids: List of multiple FDC ID's
        :param format_: Optional. 'abridged' for an abridged set of elements, 'full' for all elements (default).
        :param nutrients: Optional. List of up to 25 nutrient numbers. Only the nutrient
        information for the specified nutrients will be returned. Should be comma separated list (e.g. nutrients=203,
        204) or repeating parameters (e.g. nutrients=203&nutrients=204). If a food does not have any matching
        nutrients, the food will be returned with an empty foodNutrients element.
        :return: List of `str` jsons
        """
        req = self._call_foods(ids, format_, nutrients)
        return req.text

    def _call_foods(self, ids: List[str], format_: str = "full", nutrients: List[int] = None) -> requests.Response:
        url = self.base_url + f"foods?api_key={self.api_key}&format={format_}"
        for fdc_id in ids:
            url += f"&fdcIds={fdc_id}"
        if nutrients:
            url += f"&nutrients={nutrients}"
        req = requests.get(url)
        if req.status_code != 200:
            req.raise_for_status()
        return req

    def get_foods_list(self, data_type: str = None, page_size: int = None, page_number: int = None, sort_by: str = None,
                       sort_order: str = None) -> list[AbridgedFood.AbridgedFood]:
        """
        Retrieves a paged list of foods. Use the pageNumber parameter to page through the entire result set.
        :param data_type: Optional. Filter on a specific data type; specify one or more values in an array.
        :param page_size: Optional. Maximum number of results to return for the current page. Default is 50. Min=1, Max=200
        :param page_number: Optional. Page number to retrieve. The offset into the overall result set is expressed as
        (pageNumber * pageSize)
        :param sort_by: Optional. Specify one of the possible values to sort by that field. Note, dataType.keyword will
        be dataType and lowercaseDescription.keyword will be description in future releases. Can be any of the following
        `["dataType.keyword", "lowercaseDescription.keyword", "fdcId", "publishedDate"]`
        :param sort_order: Optional. The sort direction for the results. Only applicable if sortBy is specified.
        Can be any of the following `["asc", "desc"]`
        :return: List of `AbridgedFood` objects
        """
        req = self._call_foods_list(data_type, page_size, page_number, sort_by, sort_order)
        result_json = humps.decamelize(json.loads(req.text))
        foods = []
        for item in result_json:
            food = AbridgedFood.AbridgedFood(**item)
            foods.append(food)
        return foods

    def get_foods_list_raw(self, data_type: str = None, page_size: int = None, page_number: int = None,
                           sort_by: str = None, sort_order: str = None) -> str:
        """
        Retrieves a paged list of foods. Use the pageNumber parameter to page through the entire result set.
        :param data_type: Optional. Filter on a specific data type; specify one or more values in an array.
        :param page_size: Optional. Maximum number of results to return for the current page. Default is 50. Min=1, Max=200
        :param page_number: Optional. Page number to retrieve. The offset into the overall result set is expressed as
        (pageNumber * pageSize)
        :param sort_by: Optional. Specify one of the possible values to sort by that field. Note, dataType.keyword will
        be dataType and lowercaseDescription.keyword will be description in future releases. Can be any of the following
        `["dataType.keyword", "lowercaseDescription.keyword", "fdcId", "publishedDate"]`
        :param sort_order: Optional. The sort direction for the results. Only applicable if sortBy is specified.
        Can be any of the following `["asc", "desc"]`
        :return: List of `str` jsons
        """
        req = self._call_foods_list(data_type, page_size, page_number, sort_by, sort_order)
        return req.text

    def _call_foods_list(self, data_type: str = None, page_size: int = None, page_number: int = None,
                         sort_by: str = None, sort_order: str = None) -> requests.Response:
        url = self.base_url + f"foods/list?api_key={self.api_key}"
        if data_type:
            url += f"&dataType={data_type}"
        if page_size:
            url += f"&pageSize={page_size}"
        if page_number:
            url += f"&pageNumber={page_number}"
        if sort_by:
            url += f"&sortBy={sort_by}"
        if sort_order:
            url += f"&sortOrder={sort_order}"
        req = requests.get(url)
        if req.status_code != 200:
            req.raise_for_status()
        return req

    def get_foods_search(self, query: str, data_type: str = None, page_size: int = None, page_number: int = None,
                         sort_by: str = None, sort_order: str = None, brand_owner: str = None) \
            -> SearchResult.SearchResult:
        """
        Search for foods using keywords. Results can be filtered by dataType and there are options for result page sizes
         or sorting.
        :param query: One or more search terms. The string may include search operators:
        https://fdc.nal.usda.gov/help.html#bkmk-2
        :param data_type: Optional. Filter on a specific data type; specify one or more values in an array.
        Available values : Branded, Foundation, Survey (FNDDS), SR Legacy
        :param page_size: Optional. Maximum number of results to return for the current page. Default is 50. Min is 1,
        Max is 200
        :param page_number: Optional. Page number to retrieve. The offset into the overall result set is expressed as
         (pageNumber * pageSize)
        :param sort_by: Optional. Specify one of the possible values to sort by that field. Note, dataType.keyword will
         be dataType and lowercaseDescription.keyword will be description in future releases.
        Available values : dataType.keyword, lowercaseDescription.keyword, fdcId, publishedDate
        :param sort_order: Optional. The sort direction for the results. Only applicable if sortBy is specified.
        Available values : asc, desc
        :param brand_owner: Optional. Filter results based on the brand owner of the food. Only applies to Branded Foods
        :return: `str` or `SearchResult` object
        """
        req = self._call_foods_search(query, data_type, page_size, page_number, sort_by, sort_order, brand_owner)
        result_json = humps.decamelize(json.loads(req.text))
        search_result = SearchResult.SearchResult(**result_json)
        return search_result

    def get_foods_search_raw(self, query: str, data_type: str = None, page_size: int = None, page_number: int = None,
                             sort_by: str = None, sort_order: str = None, brand_owner: str = None) -> str:
        """
        Search for foods using keywords. Results can be filtered by dataType and there are options for result page sizes
        or sorting.
        :param query: One or more search terms. The string may include search operators:
        https://fdc.nal.usda.gov/help.html#bkmk-2
        :param data_type: Optional. Filter on a specific data type; specify one or more values in an array.
        Available values : Branded, Foundation, Survey (FNDDS), SR Legacy
        :param page_size: Optional. Maximum number of results to return for the current page. Default is 50. Min is 1,
        Max is 200
        :param page_number: Optional. Page number to retrieve. The offset into the overall result set is expressed as
         (pageNumber * pageSize)
        :param sort_by: Optional. Specify one of the possible values to sort by that field. Note, dataType.keyword will
         be dataType and lowercaseDescription.keyword will be description in future releases.
        Available values : dataType.keyword, lowercaseDescription.keyword, fdcId, publishedDate
        :param sort_order: Optional. The sort direction for the results. Only applicable if sortBy is specified.
        Available values : asc, desc
        :param brand_owner: Optional. Filter results based on the brand owner of the food. Only applies to Branded Foods
        :return: `str` of json
        """
        req = self._call_foods_search(query, data_type, page_size, page_number, sort_by, sort_order, brand_owner)
        return req.text

    def _call_foods_search(self, query: str, data_type: str = None, page_size: int = None, page_number: int = None,
                           sort_by: str = None, sort_order: str = None, brand_owner: str = None) \
            -> requests.Response:
        url = self.base_url + f"foods/search?api_key={self.api_key}&query={query}"
        if data_type:
            url += f"&dataType={data_type}"
        if page_size:
            url += f"&pageSize={page_size}"
        if page_number:
            url += f"&pageNumber={page_number}"
        if sort_by:
            url += f"&sortBy={sort_by}"
        if sort_order:
            url += f"&sortOrder={sort_order}"
        if brand_owner:
            url += f"&brandOwner={brand_owner}"
        req = requests.get(url)
        if req.status_code != 200:
            req.raise_for_status()
        return req

    def get_json_specs(self) -> str:
        """
        The OpenAPI 3.0 specification for the FDC API rendered as JSON (JavaScript Object Notation)
        :return: Returns the documentation found at https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1
        in JSON notation
        """
        url = self.base_url + f"json-spec?api_key={self.api_key}"
        req = requests.get(url)
        if req.status_code != 200:
            req.raise_for_status()
        return req.text

    def get_yaml_specs(self) -> str:
        """
        The OpenAPI 3.0 specification for the FDC API rendered as YAML (YAML Ain't Markup Language)
        :return: Returns the documentation found at https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1
        in YAML notation
        """
        url = self.base_url + f"yaml-spec?api_key={self.api_key}"
        req = requests.get(url)
        if req.status_code != 200:
            req.raise_for_status()
        return req.text

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
        elif item["data_type"] == "Experimental":
            food = ExperimentalFood.ExperimentalFood(**item)
        else:
            print(f"Unexpected DataType: {item['data_type']}")
        return food


if __name__ == "__main__":
    with open("../../config.json", "r") as file:
        json_file = json.load(file)
        key = json_file["api_key"]
    fdc = FDC(key)
    x = fdc.get_foods_list_raw()
    # for i in range(100):
    #    x = fdc.get_food(str(2262077 + i), format_="abridged")
    # x = fdc.get_foods(["2262077", "2262077"], "full")
    print(x)
