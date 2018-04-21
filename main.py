import os
import shutil
import zipfile

# main variables
t_folder = 'KT_Temp'
f_folder = 'Final_Karaoke'
s_folder = 'KaraokeSCCDs'
temp = os.path.abspath(os.path.join('/', 'home', 'chris', 'Temp', t_folder))
final = os.path.abspath(os.path.join('/', 'home', 'chris', 'Work', f_folder))
work = os.path.abspath(os.path.join('/', 'home', 'chris', 'Work', s_folder))
stop_count = 100
file_count = 0


def test_paths():
    if not os.path.isdir(temp):
        log_info('The Temp location {0} does not exist.  Can not proceed further.'.format(t_folder))
        return False
    if not os.path.isdir(final):
        log_info('The Work location {0} does not exist.  Can not proceed further.'.format(f_folder))
        return False
    if not os.path.isdir(work):
        log_info('The Main directory {0} does not exist.  Can not proceed further.'.format(s_folder))
        return False
    return True


def log_info(s):
    print('<', '*' * 58, '>')
    print(s)
    print('<', '*' * 58, '>')


def file_count_check():
    if file_count < stop_count:
        file_count += 1
        return True
    return False


def move_cdg(cdg_list):
    pass


def move_zip(zip_list):
    pass


def main():
    if not test_paths():
        exit()

    folder_list = []
    zip_list = []
    file_list = []
    bad_entries = []

    for entry in os.listdir(work):
        _ = os.path.join(work, entry)
        if os.path.isdir(_):
            folder_list.append(entry)
        else:
            file_name, file_ext = os.path.splitext(entry)
            if file_ext == '.zip':
                zip_list.append(file_name)
            else:
                if file_ext == '.cdg':
                    # cdg should have a corresponding mp3 file - if so - we have a matched pair so file name is good
                    if os.path.isfile(file_name + '.mp3'):
                        file_list.append(file_name)
                    else:
                        bad_entries.append(entry)
                else:
                    if not file_ext == '.mp3':
                        bad_entries.append(entry)

    # process cdg files
    if file_list:
        move_cdg(file_list)
    if file_count_check() and zip_list:
        move_zip(zip_list)
    log_info('Folders: \n' + '\n'.join(folder_list))
    log_info('Zips: \n' + '\n'.join(zip_list))
    log_info('CDGs: \n' + '\n'.join(file_list))
    log_info('Bad Entries: \n' + '\n'.join(bad_entries))

    # while file_number < 52:
    #     the_path = dir_start + str(file_number) + dir_end
    #     process(the_path, file_number)
    #     if file_number == 43:
    #         the_path = dir_start + str(file_number) + ' Missing CDG Files'
    #         process(the_path, file_number)
    #     shutil.rmtree(the_path)
    #     file_number += 1


if __name__ == '__main__':
    main()
