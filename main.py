import data
import re
import zipfile
from pathlib import Path


def test_paths():
    """
    test the folders/directories the program will be using to verify that they exist -
    may eventually turn this into option to select - but for now they are set in the main variables
    :return: false for any directory that is missing, otherwise true if all directories are verified
    """
    if not working_dir.is_dir():
        print_messages(f'The Temp location {working_dir} does not exist.\nCan not proceed further.')
        return False
    if not finished_dir.is_dir():
        print_messages(f'The Work location {finished_dir} does not exist.\nCan not proceed further.')
        return False
    if not original_dir.is_dir():
        print_messages(f'The Main directory {original_dir} does not exist.\nCan not proceed further.')
        return False
    return True


# def count_current_items():
#     global file_count
#     for _ in os.listdir(temp):
#         file_count += 1
#
#
def print_messages(message, open=True, close=True):
    """
    prints nicely formatted messages to the screen
    :param message: message to printed
    :param open: boolean - show the opening bar
    :param close: boolean - show the closing bar
    :return: n/a
    """
    if open:
        print('<', '*' * 78, '>')
    print(message)
    if close:
        print('<', '*' * 78, '>')
#
#
# def is_under_file_count():
#     global file_count
#     if file_count < stop_count:
#         file_count += 2
#         return True
#     return False
#
#
# def proc_folder(folder):
#     for _ in os.listdir(folder):
#         entry = os.path.join(folder, _)
#         if os.path.isdir(entry):
#             proc_folder(entry)
#         else:
#             proc_file(entry)
#
#
# def proc_file(full_file):
#     path = os.path.dirname(full_file)
#     file = os.path.basename(full_file)
#     name, ext = os.path.splitext(file)
#     if ext.lower() == ".zip":
#         proc_zip(full_file)
#     elif ext == ".CDG":
#         fix_cdg(path, name)
#     elif ext == ".cdg":
#         proc_cdg(path, name)
#     else:
#         extraneous.append(full_file)
#
#
# def proc_zip(zip):
#     pass
#
#
# def fix_cdg(path, name):
#     os.rename("{0}/{1}.CDG".format(path, name), "{0}/{1}.cdg".format(path, name))
#     # test mp3 portion
#     if os.path.isfile("{0}/{1}.MP3".format(path, name)):
#         os.rename("{0}/{1}.MP3".format(path, name), "{0}/{1}.mp3".format(path, name))
#     proc_cdg(path, name)
#
#
# def proc_cdg(path, file):
#     if is_under_file_count():
#         shutil.move("{0}/{1}.cdg".format(path, file), "{0}/{1}.cdg".format(temp, file))
#         shutil.move("{0}/{1}.mp3".format(path, file), "{0}/{1}.mp3".format(temp, file))
#
#
# def proc_temp():
#     for file in os.listdir(temp):
#         if re.match(standard_patt, file):
#             print(file + ' is a STANDARD match')
#         elif re.match(no_abbr_patt, file):
#             proc_no_abbreviation(file)added db update #1 function to db class
#
#
# def proc_no_abbreviation(file):
#     r = re.match(no_abbr_patt, file)
#     entry = Record(abbr='', disc=r.group(1), track=r.group(2), artist=r.group(3), song=r.group(4), aid=0, sid=0)
#     if not validate_record(entry):
#         print('Problem validating ' + file)
#         exit()
#     options(entry)
#
#
# def options(record):
#     """
#     goes through the individual options - assumes that record is a valid reference to the namedtuple Record
#     current available options
#         ENTER/RETURN - Add to DB (and move file to Final location)
#         W - Swap Song and Artist
#     :param record: an instance of the nametuple Record
#     :return:
#     """
#     print_record_info(record)
#     exit()
#
#
# def print_record_info(record):
#     """
#     prints the record info to the screen
#     :param record:  a valid instance of namedtuple Record
#     :return: nothing
#     """
#     print("*" * 80)
#     print("Disc Reference: {0}{1}-{2}".format(record.abbr, record.disc, record.track))
#     print("Song Artist: {}".format(record.artist))
#     print("Song Title: {}".format(record.song))
#     print("*" * 80)
#
#
# def validate_record(item):
#     if item.abbr == '':
#         if default_abbr == '':
#             set_default_abbr()
#         print("default abbr = " + default_abbr)
#         item._replace(abbr=default_abbr)
#
#     if not item.disc.isdigit():
#         result = input("Your disc contains non-numeric data - does this need corrected(y/N)?")
#         if result.upper() == 'Y':
#             while not result.isdigit():
#                 result = input("You new ALL NUMERIC disc number: ")
#             item._replace(disc=result)
#
#     if not item.track.isdigit():
#         result = input("Your track contains non-numeric data - does this need corrected(y/N)?")
#         if result.upper() == 'Y':
#             while not result.isdigit():
#                 result = input("You new ALL NUMERIC track number: ")
#             item._replace(track=result)
#
#     if not item.artist == '' and not item.song == '':
#         print_record_info(item)
#         return True
#
#     return False
#
#
# def set_default_abbr():
#     global default_abbr
#     abbr = input("Please enter a default abbreviation: ")
#     if len(abbr) < 2 or len(abbr) > 4:
#         print("Your abbreviation must have at least 2 characters, and no more than 4 characters.")
#         set_default_abbr()
#     elif not abbr.isalpha():
#         print("Your abbreviation must contain only A - Z, no spaces, punctuation or numbers.")
#         set_default_abbr()
#     else:
#         default_abbr = abbr.upper()


def main():
    """
    This is our main program
    :return: nothing is returned as this is the main function
    """
    if not test_paths():
        exit()
    # data.db_first_launch(music_db)
    # data.make_tables(music_db)
    #
    # count_current_items()
    #
    # # do some configs
    # if default_abbr == '':
    #     set_default_abbr()
    #
    # if file_count == 0:
    #     proc_folder(work)
    #
    # if file_count > 0:
    #     proc_temp()


if __name__ == '__main__':
    music_db = Path.home() / '.databases' / 'music.db'
    working_dir = Path.home() / 'Temp' / 'KT_Temp'
    original_dir = Path.home() / 'Work' / 'KaraokeSCCDs'
    finished_dir = Path.home() / 'Work' / 'Final_Karaoke'

    standard_patt = "^([A-Z]{2,4})(\d+)-([0-9]{2})\s-\s([\w ]+)\s-\s([\w \']+).cdg|mp3$"
    no_abbr_patt = "^(\d+)-([0-9]{2})\s?-\s?([\w ]+)\s-\s([\w \']+).cdg|mp3$"
    stop_count = 200
    file_count = 0
    extraneous = []
    default_abbr = ''

    main()
