from datetime import datetime


def to_array(a):
    arr = [row for row in a]
    return arr


def apply_and_to_array(a, func):
    arr = [func(row) for row in a]
    return arr


def format_date(dt):
    return dt.strftime("%m/%d/%Y %H:%M:%S")


def date_diff_to_today(dt):
    now = datetime.now()
    delta = dt - now
    return delta.days
