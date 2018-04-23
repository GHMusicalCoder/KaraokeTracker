import os
import shutil
import zipfile

# main variables
stop_count = 200
file_count = 0
t_folder = 'KT_Temp'
f_folder = 'Final_Karaoke'
s_folder = 'KaraokeSCCDs'
temp = os.path.abspath(os.path.join('/', 'home', 'chris', 'Temp', t_folder))
final = os.path.abspath(os.path.join('/', 'home', 'chris', 'Work', f_folder))
work = os.path.abspath(os.path.join('/', 'home', 'chris', 'Work', s_folder))
extraneous = []


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


def count_current_items():
    global file_count
    for _ in os.listdir(temp):
        file_count += 1


def log_info(s):
    print('<', '*' * 58, '>')
    print(s)
    print('<', '*' * 58, '>')


def is_under_file_count():
    global file_count
    if file_count < stop_count:
        file_count += 2
        return True
    return False


def proc_folder(folder):
    for _ in os.listdir(folder):
        entry = os.path.join(folder, _)
        if os.path.isdir(entry):
            proc_folder(entry)
        else:
            proc_file(entry)


def proc_file(full_file):
    path = os.path.dirname(full_file)
    file = os.path.basename(full_file)
    name, ext = os.path.splitext(file)
    if ext.lower() == ".zip":
        proc_zip(full_file)
    elif ext == ".CDG":
        fix_cdg(path, name)
    elif ext == ".cdg":
        proc_cdg(path, name)
    else:
        extraneous.append(full_file)


def proc_zip(zip):
    pass


def fix_cdg(path, name):
    os.rename("{0}/{1}.CDG".format(path, name), "{0}/{1}.cdg".format(path, name))
    # test mp3 portion
    if os.path.isfile("{0}/{1}.MP3".format(path, name)):
        os.rename("{0}/{1}.MP3".format(path, name), "{0}/{1}.mp3".format(path, name))
    proc_cdg(path, name)


def proc_cdg(path, file):
    if is_under_file_count():
        shutil.move("{0}/{1}.cdg".format(path, file), "{0}/{1}.cdg".format(temp, file))
        shutil.move("{0}/{1}.mp3".format(path, file), "{0}/{1}.mp3".format(temp, file))


def main():
    if not test_paths():
        exit()

    count_current_items()
    proc_folder(work)
    if file_count > 0:
        # start processing temp folder
        pass


if __name__ == '__main__':
    main()
