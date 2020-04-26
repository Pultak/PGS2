from Structure import Structure
import Structure


class TXTParser:

    def __init__(self, stats):
        self.stats = stats

    def parse(self, input_file):
        for line in input_file:
            parts = line.split(';')

            if parts[Structure.ACTION_TYPE_INDEX] == "insert":
                self.stats.insert_record(parts)
            elif parts[Structure.ACTION_TYPE_INDEX] == "delete":
                self.stats.delete_record(parts)
            else:
                print("UNKNOWN ACTION %s" % parts[ACTION_TYPE_INDEX])


