import os
import shutil as sh

def make_directories(scan_dir, path_to_dirs='.'):
    """
    Create a set of nested directories based on the keys of the input dictionary. The keys refer to parameters in the input
    files and the directory values refer to the scanned values. For example, the input directory may be:

    scan_dir = {'te': [10,20,30], 'ti': [15,30], 'nx': [128, 256, 512, 1024]}.

    The resulting directory tree may then read:

    path_to_dirs/
    ├── te_10/
    │   ├── ti_15/
    │   │   ├── nx_128/BOUT.inp
    │   │   ├── nx_256/BOUT.inp
    │   │   ├── nx_512/BOUT.inp
    │   │   └── 1024/BOUT.inp
    │   └── ti__30/
    │       ├── nx_128/BOUT.inp
    │       ├── nx_256/BOUT.inp
    │       ├── nx_512/BOUT.inp
    │       └── nx_1024/BOUT.inp
    ├── te_20/
    │   ├── ti_15/
    │   │   ├── nx_128/BOUT.inp
    │   │   ├── nx_256/BOUT.inp
    │   │   ├── nx_512/BOUT.inp
    │   │   └── nx_1024/BOUT.inp
    │   └── ti_30/
    │       ├── nx_128/BOUT.inp
    │       ├── nx_256/BOUT.inp
    │       ├── nx_512/BOUT.inp
    │       └── nx_1024/BOUT.inp
    └── te_30/
        ├── ti_15/
        │   ├── nx_128/BOUT.inp
        │   ├── nx_256/BOUT.inp
        │   ├── nx_512/BOUT.inp
        │   └── nx_1024/BOUT.inp
        └── ti_30
            ├── nx_128/BOUT.inp
            ├── nx_256/BOUT.inp
            ├── nx_512/BOUT.inp
            └── nx_1024/BOUT.inp

    Args:
        path_to_dirs: String, path to location of directories, default is '.'
        scan_dir: Dictionary of the from {key=string, values=list}

    Returns:

    Raises:

    """

    parent_dirs = [path_to_dirs]
    for scan in scan_dir:
        append_to_parent_dirs = []
        while len(parent_dirs):
            parent = parent_dirs[0]
            for param in scan_dir[scan]:
                dir_name = parent + '/' + scan + '_' + str(param)
                append_to_parent_dirs.append(dir_name)
                os.makedirs(dir_name)
                make_input_file(parent, dir_name)
            parent_dirs.remove(parent)
            remove_input_file(parent)
        parent_dirs += append_to_parent_dirs


def make_input_file(template_location, target_location):
    """
    Copies BOUT.inp file template_location to target_location, and modifies the input parameters according to the
    relative path. For example, if the template is located at ti_30 and the target is ti_30/nx_512 the new input
    file will have its nx parameter value changed to 512.

    Args:
        template_location: String, path to location of template input file
        target_location: String, path to location of target input file

    Returns:

    Raises:
    """
    sh.copy2(template_location+'/BOUT.inp',target_location)
    
    with open(target_location+'/BOUT.inp', 'r') as file:
        input_file = file.readlines()
    
    par_val = target_location.split('/')[-1]
    par = par_val.split('_')[0]
    val = par_val.split('_')[1]
    
    for num, line in enumerate(input_file):
        if line[:len(par)].lower() == par.lower():
            line = line.split(' ')
            for char in line[line.index('=')+1:]:
                if char != '':
                    line[line.index(char)] = val
                    break
            line = ' '.join(line) + '\n'
            input_file[num] = line
            break
    
    with open(target_location+'/BOUT.inp', 'w') as file:
        file.writelines(input_file)

def remove_input_file(file_location):
    """
    Removes BOUT.inp file at file_location
    Args:
        file_location: String, path to location of input file

    Returns:

    Raises:
    """
    os.remove(file_location + '/BOUT.inp')

# scan = {'te0': [10, 20, 30], 'ti0': [15, 30], 'nx': [128, 256, 512, 1024]}
# make_directories(scan, 'parameter_scan')