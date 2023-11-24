from .FoodNutrientSource import FoodNutrientSource


class FoodNutritionDerivation:
    def __init__(self, id: int, code: str, description: str, food_nutrient_source: dict):
        self.id = id
        self.code = code
        self.description = description
        self.food_nutrient_source = FoodNutrientSource(**food_nutrient_source)