from .Food import Food
from .FoodCategory import FoodCategory
from .FoodNutrient import FoodNutrient
from .NutrientConversionFactor import NutrientConversionFactor
from datetime import datetime


class SRLegacyFood(Food):
    def __init__(self, fdc_id: int, data_type: str, description: str, food_class: str = None,
                 is_historical_reference: bool = None, ndb_number: int = None, publication_date: str = None,
                 scientific_name: str = None, food_category: dict = None,
                 food_nutrients: dict = None,
                 nutrient_conversion_factors: dict = None):
        super().__init__()
        self.fdc_id = fdc_id
        self.data_type = data_type
        self.description = description
        self.food_class = food_class
        self.is_historical_reference = is_historical_reference
        self.ndb_number = ndb_number
        try:
            self.publication_date = datetime.strptime(publication_date, "%m/%d/%Y").date()
        except ValueError:
            # If we are using list_foods, we get a different format for some reason
            self.publication_date = datetime.strptime(publication_date,
                                                      "%Y-%m-%d").date() if publication_date else publication_date
        self.scientific_name = scientific_name
        self.food_category = FoodCategory(**food_category) if food_category else None
        self.food_nutrients = [FoodNutrient(**food_nutrient) for food_nutrient in food_nutrients] if food_nutrients else food_nutrients
        self.nutrient_conversion_factors = [NutrientConversionFactor(**nutrient_conversion_factor) for
                                            nutrient_conversion_factor in nutrient_conversion_factors] if nutrient_conversion_factors else nutrient_conversion_factors
