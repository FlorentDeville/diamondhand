class DbCsv:

    def __init__(self):
        pass

    # Scrap a single card information from the url and return a db.Entry
    def scrap_card_information(self, url, set_code):
        pass

    # Write a new entry to the csv database
    def write(self, entry):
        new_line = "{};\"{}\";\"{}\";\"{}\";{};{};{};{}\n"
        new_line = new_line.format(entry.id, entry.set_name, entry.set_code, entry.name, entry.number, entry.rarity, entry.tcg_url, entry.variation)
        with open(self.m_csvFilename, "a") as f:
            f.write(new_line)

    # Load the db
    def load(self):
        entries = []
        with open(self.m_csvFilename) as csvFile:
            lines = csv.reader(csvFile, delimiter=';', quotechar='"')
            for line in lines:
                newEntry = Entry()
                if len(line) == 0:  # empty line
                    continue
                newEntry.id = line[0]
                newEntry.set_name = line[1]
                newEntry.set_code = line[2]
                newEntry.name = line[3]
                newEntry.number = line[4]
                newEntry.rarity = line[5]
                newEntry.tcg_url = line[6]
                newEntry.variation = line[7]
                if len(line) > 8 and line[8] == '1':
                    newEntry.own = True
                else:
                    newEntry.own = False
                entries.append(newEntry)

        return entries

    def raw_name_to_printed_name(self, entry):
        entry.printed_name = entry.name
