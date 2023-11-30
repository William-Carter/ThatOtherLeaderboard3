import cobble.validations


class IsLBDirection(cobble.validations.Validation):
    def __init__(self) -> None:
        """
        Validate that an input is either "asc" or "desc"
        """
        self.requirements = "Must be either 'asc' or 'desc'"
    def validate(self, x: str) -> bool:
        """
        Determines whether a given input is a valid integer
        Parameters:
            x - the input to test
        Returns:
            valid - True if the input is a valid integer, False otherwise
        """
        return x.lower() in ['asc', 'desc']

        