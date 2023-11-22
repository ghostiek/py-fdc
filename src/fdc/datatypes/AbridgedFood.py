from .AbridgedFoodNutrient import AbridgedFoodNutrient

from datetime import datetime


class AbridgedFood:
    def __init__(self, fdc_id, description, publication_date, food_nutrients, data_type, ndb_number):
        self.fdc_id = fdc_id
        self.description = description
        self.publication_date = datetime.strptime(publication_date, "%Y-%m-%d").date()
        self.food_nutrients = [AbridgedFoodNutrient(**food_nutrient) for food_nutrient in food_nutrients]
        self.data_type = data_type
        self.ndb_number = ndb_number

