from .Nutrient import Nutrient

class FoodNutrient:
    def __init__(self, nutrient, type, food_nutrient_derivation=None, id=None, amount=None, data_points=None, max=None,
                 min=None, median=None, min_year_acquired=None, nutrient_analysis_details=None, loq=None):
        self.Nutrient = Nutrient(**nutrient)
        self.type = type
        self.food_nutrient_derivation = food_nutrient_derivation
        self.id = id
        self.amount = amount
        self.data_points = data_points
        self.max = max
        self.min = min
        self.median = median
        self.min_year_acquired = min_year_acquired
        self.nutrient_analysis_details = nutrient_analysis_details
        self.loq = loq