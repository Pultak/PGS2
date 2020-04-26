from xml.sax import handler, make_parser
from xml.sax.xmlreader import XMLReader

from Structure import *


class XMLParser(handler.ContentHandler):

    def __init__(self, stats):
        super().__init__()
        self.stats = stats
        self.content = ""

        self.actual_user = None
        self.activity_type = None
        self.actual_timetable_action = None
        self.department = None
        self.get_subject = False
        self.subject = None
        self.subject_kind = None
        self.season = None

    def startElement(self, name, attrs):
        if name == "actor":
            self.actual_user = attrs["personalNumber"]
        elif name == "processedData":
            self.activity_type = attrs["activity"]
        elif name == "timetableAction":
            self.actual_timetable_action = attrs["tt:id"]
        elif name == "tt:subject":
            self.get_subject = True
            self.subject_kind = attrs["kind"]
        self.content = ""

    def characters(self, content):
        self.content += content

    def endElement(self, name):
        if self.get_subject:
            self.subject = self.content
            self.get_subject = False
        elif name == "tt:department":
            self.department = self.content
        elif name == "tt:term":
            self.season = self.content
        elif name == "event":
            parts = [self.actual_user, self.activity_type, self.actual_timetable_action, self.department, self.subject,
                     self.subject_kind, self.season]
            if self.activity_type == "insert":
                self.stats.insert_record(parts)
            elif self.activity_type == "delete":
                self.stats.delete_record(parts)
            else:
                print("Unknown action %s!" % self.activity_type)

    def parse(self, input_file):
        parser = make_parser()
        parser.setContentHandler(self)
        parser.parse(input_file)





