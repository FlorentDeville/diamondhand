class DbCsv:

    def __init__(self):
        pass

    # Scrap a single card information from the url and return a db.Entry
    def scrap_card_information(self, url, set_code):
        pass

    # Write a new entry to the csv database
    def write(self, entry):
        pass

    # Load the db
    def load(self):
        pass

    def raw_name_to_printed_name(self, entry):
        entry.printed_name = entry.name
