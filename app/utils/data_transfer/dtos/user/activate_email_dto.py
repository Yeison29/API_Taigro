
class ActivateEmailDTO:
    def __init__(self,
                 email: str,
                 activation_code: str):
        self.email = email
        self.activation_code = activation_code
