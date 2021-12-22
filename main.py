import sqlite3
import base64
import imageio
import cv2

PASSWORD = "tempuser"

connect = input("Enter password\n")

while connect != PASSWORD:
    connect = input("Incorrect password, Please enter password\n")
    if connect == "q":
        break

if connect == PASSWORD:
    con = sqlite3.connect("myStorage.db")
    try:
        con.execute('''CREATE TABLE STORAGE (FULL_NAME TEXT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, EXTENSION TEXT 
        NOT NULL, FILES TEXT NOT NULL);''')
        print("Your storage has been created!\nWhat would you like to store in it?")
    except:
        print("You already have storage, what would you like to do?")

    while True:
        print("\n" + "*" * 15)
        print("Commands")
        print("o - open file")
        print("s - store file")
        print("q - quit storage")
        print("*" * 15)
        input_ = input(":")

        if input_ == "q":
            break
        if input_ == "o":
            file_type = input("What filetype would you like to open?\n")
            file_name = input("What filename would you like to open?\n")
            FILE_ = file_name + "." + file_type

            choice = con.execute("SELECT * from STORAGE WHERE FULL_NAME=" + '"' + FILE_ + '"')

            file_string = ""
            for row in choice:
                file_string = row[3]
            with open(FILE_, "wb") as f_output:
                print(file_string)
                f_output.write(base64.b64decode(file_string))

        if input_ == "s":
            PATH = input("Type in the full path to the file you want to store.\n")

            FILE_TYPES = {
                "txt": "TEXT",
                "py": "TEXT",
                "java": "TEXT",
                "jpg": "IMAGE",
                "png": "IMAGE",
                "jpeg": "IMAGE"
            }

            file_name = PATH.split("/")
            file_name = file_name[len(file_name) - 1]
            file_string = ""

            NAME = file_name.split(".")[0]
            EXTENSION = file_name.split(".")[1]

            try:
                EXTENSION = FILE_TYPES[EXTENSION]
            except:
                Exception()

            if EXTENSION == "IMAGE":
                IMAGE = cv2.imread(PATH)
                file_string = base64.b64encode(cv2.imencode(".jpg", IMAGE)[1]).decode()

            elif EXTENSION == "TEXT":
                file_string = open(PATH, "r").read()
                file_string = base64.b64encode(file_string)

            EXTENSION = file_name.split(".")[1]

            command = 'INSERT INTO STORAGE (FULL_NAME, NAME, EXTENSION, FILES) VALUES (%s, %s, %s, %s);' % (
                '"' + file_name + '"', '"' + NAME + '"', '"' + EXTENSION + '"', '"' + file_string + '"')

            con.execute(command)
            con.commit()
