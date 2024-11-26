from datetime import date

def get_age(year, month, day):
    today = date.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age
