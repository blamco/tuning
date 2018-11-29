import zipfile
import os
import shutil
import re
from collections import Counter

def get_source():
    for file in os.listdir(os.curdir):
        if file.endswith(".7z"):
            source = os.path.join(os.curdir, file)
            return source


def get_sfc_path():
    walk = list(os.walk(os.getcwd()))
    paths = []
    for i in walk:
        for j in i[-1]:
            paths.append("{}/{}".format(i[0], j).replace("\\", "/"))
    sfc_paths = list(filter(lambda x: "sfc.exe" in x and ".log" in x, paths))
    return sfc_paths


def get_max_version(list_of_paths):
    max_version = [0, 0, 0]
    r = r'\d{1,2}\.\d{1,2}\.\d{1,2}'
    for path in list_of_paths:
        reg = re.findall(r, path)
        if reg:
            if list(map(lambda x: int(x), reg[0].split("."))) > max_version:
                max_version = list(map(lambda x: int(x), reg[0].split(".")))
    return ".".join(list(map(lambda x: str(x), max_version)))


def get_version(path):
    r = r'(\d{1,2}\.\d{1,2}\.\d{1,2}).*sfc\.exe.*'
    reg = re.findall(r, path)
    if reg:
        return reg[0]
    return "0.0.0"


def get_log_files(source):
    print("Moving log files into the output directory.\n")
    with zipfile.ZipFile(source) as archive:
        namelist = []
        for x in archive.namelist():
            namelist.append(x)
        max_version = get_max_version(namelist)
        for f in archive.namelist():
            if get_version(f) == max_version:
                fname = os.path.basename(f)
                source = archive.open(f)
                target = open(os.path.join(output, fname), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
    archive.close()
    return os.listdir(output)


def print_info(data, name):
    with open("summary.txt", "a") as f:
        print("Top 10 {}:\n".format(name))
        f.write("Top 10 {}:\n".format(name))
        for i in data:
            print('{0:>8}'.format(i[1]), i[0].rstrip())
            output = '{0:>8}'.format(i[1]), i[0].rstrip()
            f.write("{} {}\n".format(str(output[0]), str(output[1])))
        print("\n\n")
        f.write("\n\n")

source = get_source().split('\\')[1]
output = "{}\\{}".format(os.getcwd(), source.split('.')[0])
try:
    if not os.path.exists(output):
        os.mkdir(output)
except OSError:
    print("Creation of the directory {} has failed.\n".format(output))
else:
    print("Successfully created the directory {}.\n".format(output))
log_files = get_log_files(source)
print("Parsing the logs.\n")
log_files2 = log_files[1:]
log_files2.append(log_files[0])
data = []
for log in log_files2:
    r = r'(\w{3} \d{1,2} \d\d:\d\d:\d\d).*Event::Handle.*\\\\\?\\(.*)\(\\\\\?\\.*\).*\\\\\?\\(.*)'
    with open(output+"/"+log, errors="ignore") as f:
        log_read = f.readlines()
    for line in log_read:
        if "Event::HandleCreation" in line:
            reg = re.findall(r, line)
            if reg:
                data.append("{},{},{}\n".format(reg[0][0], reg[0][1], reg[0][2]))

# Get Process information and print to screen and log
process_list = list(map(lambda x: x.split(',')[2], data))
common_process = Counter(process_list).most_common(10)
print_info(common_process, "Processes")

# Get File information and print to screen and log
file_list = list(map(lambda x: x.split(',')[1], data))
common_files = Counter(file_list).most_common(10)
print_info(common_files, "Files")

# Get Extension information and print to screen and log
extension_list = list(map(lambda x: x.split(',')[1], data))
extension_list_scrubbed = []
for i in extension_list:
    if '.' in i.split('\\')[-1]:
        x = i.split('.')[-1]
        extension_list_scrubbed.append(x)
common_extensions = Counter(extension_list_scrubbed).most_common(10)
print_info(common_extensions, "Extensions")

# Get Path information and print to screen and log
path_list = list(map(lambda x: x.split(',')[1], data))
path_list_scrubbed = []
for i in path_list:
    path_only = i.split('\\')[:-1]
    path_only_merged = "\\".join(path_only)
    path_list_scrubbed.append(path_only_merged)
common_paths = Counter(path_list_scrubbed).most_common(10)
print_info(common_paths, "Paths")

#Hold screen open until Enter is pressed
while re.match(u'\u23CE', input("Press Enter to exit:\n")):
    break
