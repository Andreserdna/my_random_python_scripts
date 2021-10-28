import os
import sys
import re


ppath = "C:\\Users\\avale\\Desktop\\email_test\\test_email\\t2\\"
email_address_file = os.path.join(ppath,"email_address.txt")
text_file = list()


regex = re.compile(("([a-z0-9!#$%&'*+\\/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+\\/=?^_`"
                    "{|}~-]+)*(@|\\sat\\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\\.|"
                    "\\sdot\\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

def returnFile(p,text_file):
    for r,d,f in os.walk(p):
        for items in f:
            x = os.path.join(p,items)
            if str(x).endswith("txt"):
                text_file.append(x)
    return text_file


def readTextFiles(f_path):
    matches = list()
    reg = re.compile("[a-z0-9](\\.?[a-z0-9]){5,}@g(oogle)?mail\\.com$")
    with open(f_path) as f:
        lines = [line.rstrip() for line in f]
        for l in lines:
            matches += reg.findall(l)
            print(matches)
        f.close()
    print(matches)
def file2string(fname):
    with open(fname) as f:
        return f.read().lower()
def read2(f_path):
    try:
        textfile = open(f_path)
        readL = textfile.read()
        x = re.findall("[a-z0-9](\\.?[a-z0-9]){5,}@g(oogle)?mail\\.com$",readL)
        if len(x) > 0:
            print(x)
        y = re.findall("^[a-z0-9](\\.?[a-z0-9]){5,}@(yahoo)\\.com$",readL)
        if len(y) > 0:
            print(y)
        elif len(x +y) <= 0:
            print("no matches found!")
    except:
        print("file not found error")
def read3(f_path):
    pattern = re.compile("[a-z0-9](\\.?[a-z0-9]){5,}@g(oogle)?mail\\.com$")
    for i, line in enumerate(open(f_path)):
        for match in re.finditer(pattern,line):
            print(match)
            print("Found on line{}:{}".format(i+1, match.group()))

def read_file4(my_file):
    return (email[0] for email in re.findall(regex,my_file) if not email[0].startswith("//"))

def write2TextFile(my_file,email):
    if not os.path.exists(my_file):
        f = open(my_file,'w')
        f.write(email)


def main():
    returnFile(ppath,text_file)
    count = 0
    for items in text_file:
        for email in read_file4(file2string(items)):
            count = count + 1
            print(email)
            write2TextFile(email_address_file,email)
    print("Total email addresses extracted ={}".format(count))

if __name__ == "__main__":
    main()
