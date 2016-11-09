from Tkinter import *


def printVars(param):
    pass


class ClienUI(Frame):
    def __init__(self, client):
        self.client = client
        self.content = Tk()
        self.initUI()

    def run(self):
        self.content.mainloop()
        print "YAY"

    def connectdialog(self):

        padx = 2
        pady = 2

        top = Toplevel()
        top.title("Connection Dialog")

        usernameLabel = Label(top, text = "Username:")
        usernameLabel.grid(row=0, column=0, padx=padx, pady=pady)

        usernameEntry = Entry(top)
        usernameEntry.grid(row=0, column=1, padx=padx, pady=pady)

        passwordLabel = Label(top, text = "Password:")
        passwordLabel.grid(row=1, column=0, padx=padx, pady=pady)

        passwordEntry = Entry(top, show = "*")
        passwordEntry.grid(row=1, column=1, padx=padx, pady=pady)

        ipLabel = Label(top, text="IP & Port:")
        ipLabel.grid(row=2, column=0, padx=padx, pady=pady)

        ipEntry = Entry(top)
        ipEntry.grid(row=2, column=1, padx=padx, pady=pady)

        def callback():
            print usernameEntry.get()
            print passwordEntry.get()
            print ipEntry.get()

        connectButton = Button(top, text = "Connect", command=callback)
        connectButton.pack(side="bottom", padx=padx, pady=pady)
        connectButton.grid(row=3, column=1)

    def newfile(self):
        padx = 2
        pady = 2

        top = Toplevel()
        top.title("File name here")

        closeallButton = Button(top, text="Close all")
        closeallButton.grid(row=0, column=0, padx=padx, pady=pady)

        closeclientButton = Button(top, text="Close client")
        closeclientButton.grid(row=0, column=1, padx=padx, pady=pady)

        managecollaboratorsButton = Button(top, text="Manage collaborators")
        managecollaboratorsButton.grid(row=0, column=2, padx=padx, pady=pady)

        textField = Text(top)
        textField.grid(row=1, column=0, padx = padx, pady = pady)

        connectedcollabsLabel = Label(top, text = "Currently connected collabs")
        connectedcollabsLabel.grid(row=1, column=4, padx=padx, pady=pady)

    def initUI(self):


        padx = 2
        pady = 2

        self.newtextfileButton = Button(text = "New Text File", command = self.newfile)
        self.newtextfileButton.pack(side = "left", padx = padx, pady = pady)

        self.edityourfileButton = Button(text = "Edit your file")
        self.edityourfileButton.pack(side = "right", padx = padx, pady = pady)

        self.editelsefileButton = Button(text = "Edit outside file", command = self.connectdialog)
        self.editelsefileButton.pack(side = "bottom", padx = padx, pady = pady)

        return True

    def printVars(self, un):
        print "jo"
        print un