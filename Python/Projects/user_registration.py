# Re-run this cell and examine the docstring of each function
from python_functions import validate_name, validate_email, validate_password, top_level_domains

print("validate_name\n")
print(validate_name.__doc__)
print("--------------------\n")

print("validate_email\n")
print(validate_email.__doc__) 
print("--------------------\n")

print("validate_password\n")
print(validate_password.__doc__)

# The top level domains variable is used in validate_email to approve only certain email domains
print(top_level_domains)


# USER VALIDATION FUNCTION

def validate_user(name, email, password):

    if validate_name(name) == False:
        raise ValueError("Please make sure your name is greater than 2 characters!")

    if validate_email(email) == False:
        raise ValueError("Your email address is in the incorrect format, please enter a valid email.")

    if validate_password(password) == False:
        raise ValueError("Your password is too weak, ensure that your password is greater than 8 characters, and contains a capital letter and a number.")

    return True


# USER REGISTRATION FUNCTION

def register_user(name, email, password):
    try: 
        validate_user(name, email, password)
    except:
         return False

    user = {
        "name": name,
        "email": email,
        "password": password
    }
    return user
