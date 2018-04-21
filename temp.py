



def process(dir, num):
    for folders in os.listdir(work):
        if folders == dir:
            folder = os.path.abspath(os.path.join(work, dir))
            for files in os.listdir(folder):
                filename, file_ext = os.path.splitext(files)
                if file_ext == '.rar':
                    rar = rarfile.RarFile(files)
                    new_folder = 'Rigmar D' + str(num) + 'Temp'
                    export_folder = os.path.join(work,new_folder)
                    if not os.path.exists(os.path.join(work, new_folder)):
                        os.makedirs(os.path.join(work, new_folder))
                    print(export_folder)