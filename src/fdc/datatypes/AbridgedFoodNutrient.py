from .Nutrient import Nutrient


class AbridgedFoodNutrient:
    def __init__(self,number, name, amount, unit_name, derivation_code, derivation_description):
        self.number = number
        self.name = name
        self.amount = amount
        self.unit_name = unit_name
        self.derivation_code = derivation_code
        self.derivation_description = derivation_description