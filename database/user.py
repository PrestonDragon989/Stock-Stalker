from database.db import *

from datetime import datetime


today = datetime.today().strftime('%m-%d-%y')


def user_exists(user_name):
    data = user_data.find_one({"name": user_name})
    if data:
        return True
    return False


def request_exists(request_name):
    data = request_data.find_one({"name": request_name})
    if data:
        return True
    return False


def date_created_exists(date):
    data = user_data.find_one({"date_created": date})
    if data:
        return True
    return False


def add_user(name, preferred_name, password, clearance):
    if not user_exists(name):
        insert = {"name": name, "preferred_name": preferred_name, "password": password,
                  "date_created": today, "last_login": today, "clearance": clearance}
        update_result = user_data.insert_one(insert)
        print("ADDED USER:", update_result.inserted_id)
        return True
    return False


def remove_user(name):
    if user_exists(name):
        user_data.delete_one({"name": name})
        return True
    return False


def remove_request(name):
    if request_exists(name):
        request_data.delete_one({"name": name})
        return True
    return False


def get_data(name):
    if user_exists(name):
        query = {"name": name}
        result = user_data.find_one(query)
        return result
    return False


def login_check(name, password):
    if user_exists(name):
        if get_data(name)["password"] == password:
            return True
    return False


def add_request(name, preferred_name, password, explanation):
    insert = {"name": name, "preferred_name": preferred_name, "password": password, "explanation": explanation, "date": today}
    request_data.insert_one(insert)


def update_last_date(name):
    update_query = {"name": name}
    update_value = {"$set": {"last_login": today}}
    user_data.update_one(update_query, update_value)


def set_user_data(name, color_palette):
    user_stock = stock_data.find_one({"name": name})
    user_preferences = preferences_data.find_one({"name": name})

    if not user_stock:
        stock_insert = {"name": name, "followed": [], "placeholder_stocks": {}}
        stock_data.insert_one(stock_insert)
    if not user_preferences:
        preferences_insert = color_palette.copy()
        preferences_insert["name"] = name
        preferences_data.insert_one(preferences_insert)


def get_color_palette(name):
    pref = dict(preferences_data.find_one({"name": name}))
    del pref["name"]
    return pref


def set_color_palette(name, palette):
    update_query = {"name": name}
    update_value = {"$set": dict(palette)}
    preferences_data.update_one(update_query, update_value)


def get_user_stock_data(name):
    if user_exists(name):
        query = {"name": name}
        result = stock_data.find_one(query)
        return result
    return False


def update_followed_tickers(name, followed):
    update_query = {"name": name}
    update_value = {"$set": {"followed": followed}}
    stock_data.update_one(update_query, update_value)
