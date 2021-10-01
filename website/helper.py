def hasDigit(string: str):
    return any(string.isdigit() for letter in string)

def hasSpecialCharacters(string: str):
    special_characters = "\"!@#$%^&*()-+?_=,<>/\""
    if any(char in special_characters for char in string):
        return True
    return False
