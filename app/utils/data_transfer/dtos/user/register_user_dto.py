from datetime import date


class RegisterUserDTO:
    def __init__(self,
                 first_name: str,
                 second_name: str,
                 first_last_name: str,
                 second_last_name: str,
                 email: str,
                 cell_phone: str,
                 date_of_birth: date,
                 municipality_id: int,
                 gender_id: str):
        self.first_name = first_name
        self.second_name = second_name
        self.first_last_name = first_last_name
        self.second_last_name = second_last_name
        self.email = email
        self.cell_phone = cell_phone
        self.date_of_birth = date_of_birth
        self.municipality_id = municipality_id
        self.gender_id = gender_id


class UserAuthDTO:
    def __init__(self,
                 user_id: int,
                 password: str):
        self.user_id = user_id
        self.password = password


class AddUserAuthDTO:
    def __init__(self,
                 user_id: int,
                 password: str,
                 activation_code: str,
                 fch_register: date,
                 is_activated: bool):
        self.user_id = user_id
        self.password = password
        self.activation_code = activation_code
        self.fch_register = fch_register
        self.is_activated = is_activated


class RegisterUserMongoDTO:
    def __init__(self,
                 user: int,
                 img: str):
        self.user = user
        self.img = img
