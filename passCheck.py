import string

def pass_strong(password):
    upper_case = any([1 if c in string.ascii_uppercase else 0 for c in password])
    lower_case = any([1 if c in string.ascii_lowercase else 0 for c in password])
    special = any([1 if c in string.punctuation else 0 for c in password])
    digits = any([1 if c in string.digits else 0 for c in password])

    if not len(password) > 7 or not (upper_case and lower_case and special and digits):
        return False
    return True


