from .FoodCategory import FoodCategory
from .FoodNutrient import FoodNutrient
from .InputFoods import InputFoods
from.NutrientConversionFactor import NutrientConversionFactor
from datetime import datetime

class Food:
    def __init__(self, fdc_id, description, publication_date, food_nutrients, data_type, ndb_number, food_class,
                 input_foods, food_components, food_attributes, nutrient_conversion_factors,
                 is_historical_reference, food_category):
        self.fdc_id = fdc_id
        self.description = description
        self.publication_date = datetime.strptime(publication_date, "%m/%d/%Y").date()
        self.food_nutrients = [FoodNutrient(**food_nutrient) for food_nutrient in food_nutrients]
        self.data_type = data_type
        self.food_class = food_class
        self.input_foods = [InputFoods(**input_food) for input_food in input_foods]
        self.food_components = food_components
        self.food_attributes = food_attributes
        self.nutrient_conversion_factors = [NutrientConversionFactor(**nutrient_conversion_factor) for nutrient_conversion_factor in nutrient_conversion_factors]
        self.ndb_number = ndb_number
        self.is_historical_reference = is_historical_reference
        self.food_category = FoodCategory(**food_category)


