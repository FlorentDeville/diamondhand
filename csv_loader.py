import csv


def load_csv(csv_path):
    cards_name = []
    with open(csv_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        first_row = True
        for row in spamreader:
            if first_row:
                first_row = False
                continue

            name = row[1]
            if name is None or name == "":
                continue

            filter_row = row[4]
            if filter_row is None or filter_row == "" or filter_row == "0":
                cards_name.append(name)

    return cards_name


def load_list_csv(csv_path):
    cards = []
    with open(csv_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        #first_row = True
        for row in spamreader:
            #if first_row:
            #    first_row = False
            #    continue
            if len(row) == 0:
                continue

            code = row[0]
            col_number = row[1]

            card = {}
            card["code"] = code
            card["col_number"] = col_number
            cards.append(card)

    return cards