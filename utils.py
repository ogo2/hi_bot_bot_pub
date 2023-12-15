import re

pattern_email = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
pattern_phone = r""
def regular(email):
    if re.match(pattern_email, email) is not None:
        return True
    else:
        return False
