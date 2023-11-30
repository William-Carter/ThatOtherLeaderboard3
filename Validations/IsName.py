import cobble.validations
import re

class IsName(cobble.validations.Validation):
    def __init__(self) -> None:
        """
        Validate that an input is a valid name
        """
        self.requirements = "Must be <= 20 characters, can only contain a-z, A-Z, 0-9, ., - and _"
    def validate(self, x: str) -> bool:
        """
        Determines whether a given input is a valid integer
        Parameters:
            x - the input to test
        Returns:
            valid - True if the input is a valid integer, False otherwise
        """
        return bool(re.match(r'^[a-zA-Z0-9_.-]{1,20}$', x))


        


    
