from pydantic import BaseModel

class BmrInputs(BaseModel):
    weight: float
    height: float
    age: float


class Bmr:

    def men(self, weight, height, age):
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        return bmr

    def women(self, weight, height, age):
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 161
        return bmr