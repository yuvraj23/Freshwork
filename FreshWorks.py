import pickle
import time
import threading
import os


def DestroyData(waitigTime,obj,key,path):
        time.sleep(waitigTime)
        obj.DeleteData(key,path)
        print()

        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Alert", f"Time span of {key} Key is over, system had deleted this data from DB ")
        root.lift()









class Detail:
    User=None
    def __init__(self, ID=None, username=None,password=None):
        self.ID = ID
        self.pwd = password
        self.username = username
        self.Dict_Of_Data={}

    #1073741824

    def GetSize(self,file):
        if os.path.getsize(file) > 1073741824:
            return False
        else:
            return True

    def NewUser(self,id,name,pwd,path):
        if self.GetSize(path)==False:
            print("Operation Fail !! File Size is Greater than 1 GB")
            import sys
            sys.exit(0)


        try:
            fr = open(path, 'rb')
            found = False
            while True:
                try:
                    obj = pickle.load(fr)
                    if obj.ID == id and obj.pwd == pwd:
                        found = True

                except EOFError:
                    break
        except FileNotFoundError:
            found=False

        if found:
            print("This Email Id  already present try to login or Enter unique Email Id")
            return None
        else:
            fr = open(path, 'ab+')
            obj = Detail(id, name, pwd)
            pickle.dump(obj, fr)
            Detail.User = obj
            return obj







    def Login(self,id,pwd,path):

        fr = open(path, 'rb')
        print(path)
        while True:
            try:
                obj = pickle.load(fr)
                if obj.ID == id and obj.pwd == pwd:
                    Detail.User = obj
                    return obj
            except EOFError:
                break


        if Detail.User==None:
            print('User with given ID and password not exists make sure you have an account')





    def CreateData(self,path):
        if self.GetSize(path)==False:
            print("Operation Fail !! File Size is Greater than 1 GB")
            import sys
            sys.exit(0)

        if Detail.User==None:
            print("Please Login to add data")
        else:
            fr = open(path, 'rb')
            lst=[]
            while True:
                try:
                    obj = pickle.load(fr)
                    if obj.ID == Detail.User.username and obj.pwd == Detail.User.pwd :
                        for k in obj.Dict_Of_Data.keys():
                            lst.append(k)

                except EOFError:
                    break
            takeInput=True
            d={}
            timeSlot=None
            key = input("Enter key with unique value and None/none to Quit:")
            if key == 'None' or key == 'none':
                return Detail.User

            elif key in lst:
                print("Key already exist enter !! enter unique key")
                return Detail.User

            else:
                timeSlot = input("Enter time to live value in seconds, Enter None if you are not intrested to provided ")
                if timeSlot.lower() != 'None'.lower():
                    try:
                        timeSlot = int(timeSlot)
                    except:
                        print("Enter Int Value")
                        return Detail.User
                    value = input("Enter value : ")
                    d[key] = value
                else:
                    timeSlot=None
                    value = input("Enter value : ")
                    d[key] = value



        if len(d)==0:
            return Detail.User
        else:
            pickle_out = open(path, "rb")
            found=True
            while found:
                try:
                    obj = pickle.load(pickle_out)
                    if obj.ID == Detail.User.ID and obj.pwd == Detail.User.pwd:
                        putdata = open(path, "ab+")
                        obj.ID=Detail.User.ID
                        obj.pwd=Detail.User.pwd
                        obj.username=Detail.User.username
                        obj.Dict_Of_Data=d
                        found = False
                        pickle.dump(obj, putdata)
                        if timeSlot != None:
                            t1 = threading.Thread(target=DestroyData, args=(timeSlot,Detail.User, key,path))
                            t1.start()

                        pickle_out.close()
                        putdata.close()
                        return obj
                except EOFError:
                    break
            return Detail.User

    def ReadData(self,path):
        fr = open(path, 'rb')
        found = True
        print()
        key=input("Enter Key : ")
        print(f"Hii {Detail.User.username}, Your All Data  ",)
        print("#" * 100)
        print("#" * 100)
        d=0
        f=False
        while found:
            try:
                obj = pickle.load(fr)
                f=True
                if obj.ID == Detail.User.username and obj.pwd == Detail.User.pwd and obj.Dict_Of_Data:
                    for k in obj.Dict_Of_Data.keys():
                        if key==k:
                            print(obj.Dict_Of_Data)
                    d+=1

            except EOFError:
                if f==False:

                    print("Sorry You Don't have any Data Till Now")
                if d==0:
                    print(f"Sorry No data related to {key} KEY !!!")
                print("#" * 100)
                print("#" * 100)
                break



    def DeleteData(self,key,path):
        file =open(path,'rb')
        Found=False
        moreThanTwoValue=False
        AllData=[]
        while True:
            try:
                obj=pickle.load(file)
                if obj.ID==Detail.User.username and obj.pwd ==Detail.User.pwd and key in obj.Dict_Of_Data.keys():
                    if len(obj.Dict_Of_Data)==1:
                        Found=True
                    else:
                        Found=True
                        obj.Dict_Of_Data.pop(key)
                        AllData.append(obj)
                else:
                    AllData.append(obj)
            except EOFError:
                break
        file.close()
        if Found==False:
            print('Data not Found')
        else:
            file=open(path,'wb+')
            for data in AllData:
                pickle.dump(data,file)
            file.seek(0)
            while True:
                try:
                    obj=pickle.load(file)
                except EOFError:
                    break






if __name__ == '__main__':
    try:

        u = Detail()
        print()
        print(
            "Do you want to specify path for database else current working will be given prefrence (enter none in this case) ")
        temp = input("Enter full path  in space seprated format example: (C FolderName FileName.pkl) : ").split(" ")
        os.chdir(os.path.dirname(__file__))
        cwd = os.getcwd()
        temp_path = temp[0]
        if temp_path.lower() == 'None'.lower():
            path = cwd + "\\" + "user_data.pkl"
        else:
            path = ''
            for i in range(len(temp) - 1):
                path = path + temp[i] + " "
            path = path[0] + ":" + path[1:len(path) - 1].replace(" ", "\\").lstrip(" ")
            p = path
            import os.path

            isFile = os.path.isfile(path + "\\" + temp[len(temp) - 1])
            if isFile:
                pass
            else:

                with open(p + "\\" + temp[len(temp) - 1], 'w') as document:
                    if os.path.isfile(p + "\\" + temp[len(temp) - 1]):
                        path = p + "\\" + temp[len(temp) - 1]
                    else:
                        import sys

                        sys.exit()
                document.close()

        path = p + "\\" + temp[len(temp) - 1]
        print("Yor are working on --> ", path)
        ch = input(
            "Hello User Welcome , \n   #. Press 1 for Create New Account \n    #. Press 2 for Login \n     #. My Choice is : ").strip(
            " ")
        Log = False
        print()

        if ch == '1':
            id = input("Enter email id       : ")
            username = input('Enter username : ')
            pwd = input("Enter passwod       : ")
            print()
            u = u.NewUser(id, username, pwd, path)
            if u != None:
                u = u.Login(id, pwd, path)
                Log = True

        if ch == '2':
            id = input("Enter email id       : ")
            pwd = input("Enter passwod       : ")
            u = u.Login(id, pwd, path)
            print()
            if u != None:
                Log = True

        if Log:
            loop = True
            while loop:
                print()
                print("1 . Enter 1 for Create data ")
                print("2 . Enter 2 for Delete data ")
                print("3 . Read All Data ")
                print("4. For Exit Program")
                ch = input("Enter Choice : ")
                print()

                if ch == "1":
                    u.CreateData(path)
                elif ch == '2':
                    key = input("Enter Key of data u want to remove : ")
                    u.DeleteData(key, path)
                elif ch == '3':
                    u.ReadData(path)
                elif ch == "4":
                    import sys

                    sys.exit()
                else:
                    print("Lol !! Choice Not Found ")


        else:
            print("Please Check Your Creditenial")


    except PermissionError:
        print("Please Enter valid Path")



    except FileNotFoundError:
        print("File not found")


    except IndexError:
        print("Please Specify File name you gave one input that is for Drive")






