from datetime import datetime
from .FoodCategory import FoodCategory
from .FoodComponent import FoodComponent
from .FoodNutrient import FoodNutrient
from .InputFoods import InputFoods
from .NutrientConversionFactor import NutrientConversionFactor


class FoundationFood:
    def __init__(self, fdc_id: int, data_type: str, description: str, food_class: str = None, foot_note: str = None,
                 is_historical_reference: bool = None, ndb_number: int = None, publication_date: str = None,
                 scientific_name: str = None, food_category: dict = None, food_components: dict = None,
                 food_nutrients: dict = None, food_portion: dict = None, input_foods: dict = None,
                 nutrient_conversion_factors: dict = None, food_attributes: list = None):
        self.fdc_id = fdc_id
        self.data_type = data_type
        self.description = description
        self.food_class = food_class
        self.foot_note = foot_note
        self.is_historical_reference = is_historical_reference
        self.ndb_number = ndb_number
        self.publication_date = datetime.strptime(publication_date, "%m/%d/%Y").date()
        self.scientific_name = scientific_name
        self.food_category = FoodCategory(**food_category) if food_category else None
        self.food_components = FoodComponent(**food_components) if food_components else None
        self.food_nutrients = [FoodNutrient(**food_nutrient) for food_nutrient in food_nutrients]
        #fix this
        self.food_portion = food_portion
        self.input_foods = [InputFoods(**input_food) for input_food in input_foods]

        self.nutrient_conversion_factors = [NutrientConversionFactor(**nutrient_conversion_factor) for
                                            nutrient_conversion_factor in nutrient_conversion_factors]
        # Wasn't included in the schema but seems to be returned
        self.food_attributes = food_attributes

