import cobble.validations
import Validations.IsDuration

class IsGoldsList(cobble.validations.Validation):
    def __init__(self):
        super().__init__()
        self.requirements = "Must be a list of 18 times, separated by newlines"

    def validate(self, x: str):
        golds = x.split("\n")
        if len(golds) != 18:
            return False
        
        for gold in golds:
            if not Validations.IsDuration.IsDuration.validate("", gold):
                return False
        

        return True