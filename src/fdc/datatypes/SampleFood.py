from datetime import datetime
from .FoodComponent import FoodComponent
from .FoodNutrient import FoodNutrient
from .FoodCategory import FoodCategory


class SampleFood:
    def __init__(self, fdc_id: int, data_type: str, description: str, food_class: str = None, store_city: str = None,
                 food_attributes: list = None, food_nutrients: str = None, food_portions: list = None,
                 brand_description: str = None, sample_lot_number: str = None, food_components: list = None,
                 store_name: str = None, store_state: str = None, upc_code: str = None,
                 food_category: dict = None, publication_date: str = None):
        self.fdc_id = fdc_id
        self.description = description
        self.publication_date = datetime.strptime(publication_date, "%m/%d/%Y").date()
        self.data_type = data_type
        self.food_class = food_class
        self.food_components = [FoodComponent(**i) for i in food_components] if food_components else food_components
        self.food_attributes = food_attributes
        if food_attributes:
            print("WARNING: Class FoodAttribute was not created because it has yet to be encountered")
        self.food_nutrients = [FoodNutrient(**i) for i in food_nutrients] if food_nutrients else food_nutrients
        self.food_portions = food_portions
        if food_portions:
            print("WARNING: Class FoodPortions was not created because it has yet to be encountered")
        self.food_category = FoodCategory(**food_category) if food_category else food_category
