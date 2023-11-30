import cobble.validations
import Helpers

class IsDuration(cobble.validations.Validation):
    def __init__(self):
        super().__init__()
        self.requirements = "Must be a valid amount of time i.e. 47.5, 1:30, 1:17:27.33"

    def validate(self, x: str) -> bool:
        """
        Evaluates a given string to see if it can be parsed into a number of seconds
        Parameters:
            x - The string to be tested
        Returns:
            valid - Whether the string was successfully parsed
        """
        try:
            seconds = Helpers.durations.seconds(x)
        except:
            return False
        else:
            return True