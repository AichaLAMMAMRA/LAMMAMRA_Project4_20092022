from pathlib import Path
from tinydb import TinyDB


def create_directory(database_name):
    Path("data/").mkdir(exist_ok=True)
    try:
        database = TinyDB(f"data/{database_name}.json")
    except FileNotFoundError:
        with open(f"data/{database_name}.json", "w"):
            pass
        database = TinyDB("data/" + database_name + ".json")

    return database


def load_database(db_name):
    database = TinyDB(f"data/{db_name}.json")
    return database.all()