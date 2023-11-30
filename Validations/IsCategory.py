import cobble.validations
import json


class IsCategory(cobble.validations.Validation):
    def __init__(self) -> None:
        """
        Validate that an input is a valid category
        """
        self.requirements = "Must be a valid category. Valid categories are: oob, inbounds, unrestricted, legacy, glitchless"
    def validate(self, x: str) -> bool:
        """
        Determines whether a given input is a valid integer
        Parameters:
            x - the input to test
        Returns:
            valid - True if the input is a valid integer, False otherwise
        """
        with open("Database/CategoryPropagation.json", "r") as f:
            categories = json.load(f).keys()

        return x in categories

        