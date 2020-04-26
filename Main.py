import sys
import argparse

from XMLParser import XMLParser
from TXTParser import TXTParser
from Structure import Structure


SCRIPT_ERROR = "I/O Exception!"

input_file_name = ""
output_file_name = ""
parser = None
stats = Structure()


def check_arguments():
    """
    Function that parses inserted arguments and assign them into designed attributes
    argument -i stands for input file
             -o stands for output file
    Function also checks if the input file is in xml or txt format
    """
    global input_file_name, output_file_name, parser

    argument_parser = argparse.ArgumentParser(description="XML/TXT parser of enrollment data.")

    required_named = argument_parser.add_argument_group('required arguments')
    required_named.add_argument("-i", dest="input_file", action="store", help="Path to txt/xml input file",
                                required=True)
    argument_parser.add_argument("-o", dest="output_file", default=None, action="store", help="Path to output file. "
                                                                                "Default is vysledky-<input-file-name>")
    results = argument_parser.parse_args()

    if results.input_file.endswith(".xml"):
        parser = XMLParser(stats)
    elif results.input_file.endswith(".txt"):
        parser = TXTParser(stats)
    else:
        print("Unknown input file suffix! Terminating!")
        print(SCRIPT_ERROR)
        sys.exit(1)

    input_file_name = results.input_file
    if not results.output_file:
        last_directory_index = input_file_name.rfind('/') + 1
        output_file_name = "vysledky-%s.txt" % input_file_name[last_directory_index:-4]
    else:
        output_file_name = results.output_file


def write_down_faculties(result_file):
    """
    Function used to write down sorted faculties into output file
    :param result_file: opened output file
    """
    stats.valid_faculties.sort(key=lambda x: (x[1], x[0]))
    i = 1
    for faculty in stats.valid_faculties:
        line = "%d. %s: %d\n" % (i, faculty[0], faculty[1])
        result_file.write(line)
        i = i + 1


def write_results():
    """
    Function used to write created structure into output file
    """
    try:
        result_file = open(output_file_name, "w+")

        result_file.write("Počet všech předzápisových akcí: %d\n" % stats.inserted_actions)
        result_file.write("Počet zrušených akcí (delete): %d\n" % stats.deleted_actions)
        result_file.write("Počet skutečně zapsaných akcí: %d\n" % stats.actions_completed)
        result_file.write("Počet studentů: %d\n" % stats.student_count)
        result_file.write("Počet předmětů: %d\n" % stats.subject_count)
        result_file.write("Počet pracovišť: %d\n" % stats.faculties_count)  # write all faculties
        write_down_faculties(result_file)
        result_file.close()
    except Exception:
        print(SCRIPT_ERROR)
        sys.exit(0)


def start_parsing():
    try:
        input_file = open(input_file_name, "r")
        parser.parse(input_file)
        input_file.close()
    except IOError as e:
        print(e)
        print(SCRIPT_ERROR)
        sys.exit(0)
    except Exception as e:
        print(e)
        print(SCRIPT_ERROR)
        sys.exit(0)

    stats.get_needed_counts()


def main():
    check_arguments()
    start_parsing()
    write_results()


if __name__ == "__main__":
    main()
