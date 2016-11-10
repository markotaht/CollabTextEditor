from Tkinter import *



class ClienUI(Frame):
    def __init__(self, client):
        self.client = client
        self.content = Tk()
        self.initUI()

    def run(self):
        self.content.mainloop()
        print "YAY"

    def outsidefile(self):
        padx = 2
        pady = 2

        top = Toplevel()
        top.title("Outside file + filename")

        disconnectButton = Button(top, text="Disconnect")
        disconnectButton.grid(row=0, column=0, padx=padx, pady=pady)

        textField = Text(top)
        textField.grid(row=1, column=0, padx=padx, pady=pady)

        connectedcollabsLabel = Label(top, text="Currently connected collabs")
        connectedcollabsLabel.grid(row=1, column=4, padx=padx, pady=pady)


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
            #TODO check and connect
            print usernameEntry.get()
            print passwordEntry.get()
            print ipEntry.get()
            self.outsidefile()

        connectButton = Button(top, text = "Connect", command=callback)
        connectButton.pack(side="bottom", padx=padx, pady=pady)
        connectButton.grid(row=3, column=1)

    #updates the collaborator list
    def updatelist(self, un, pw, addnew):

        if addnew:
            print "added", un, pw
            listbox.insert(END, un + "    " + pw)

        else:
            print "edited", listbox.get(ANCHOR) + "to", un, pw
            listbox.delete(ANCHOR)
            listbox.insert(END, un+"    "+pw)

    def editdialog(self, isAddingnew):
        padx = 2
        pady = 2

        top = Toplevel()
        top.title("Edit collaborators")


        usernameLabel = Label(top, text="Username:")
        usernameLabel.grid(row=0, column=0, padx=padx, pady=pady)

        usernameEntry = Entry(top)
        usernameEntry.grid(row=0, column=1, padx=padx, pady=pady)

        passwordLabel = Label(top, text="Password:")
        passwordLabel.grid(row=1, column=0, padx=padx, pady=pady)

        passwordEntry = Entry(top)
        passwordEntry.grid(row=1, column=1, padx=padx, pady=pady)

        doneButton = Button(top, text="cancel")
        doneButton.grid(row=2, column=0, padx=padx, pady=pady)

        cancelButton = Button(top, text="done", command = lambda: self.updatelist(usernameEntry.get(), passwordEntry.get(), isAddingnew))
        cancelButton.grid(row=2, column=1, padx=padx, pady=pady)

        # TODO crashes when list is empty
        #workaround - check if there is something selected
        if listbox.get(ANCHOR)!= "":
            un = listbox.get(ANCHOR).split("    ")
            print "Editing", un
            usernameEntry.insert(0, un[0])
            passwordEntry.insert(0, un[1])


    def deletecollaborator(self):

        un = listbox.get(ANCHOR)
        print "delete", un
        listbox.delete(ANCHOR)

    def managecollaborators(self):

        padx = 2
        pady = 2

        top = Toplevel()
        top.title("Manage collaborators")

        listboxLabel = Label(top, text="username    password")
        listboxLabel.grid(row=1, column=0, padx=padx, pady=pady)

        global listbox
        listbox = Listbox(top)
        listbox.grid(row=2, column=0, padx=padx, pady=pady)
        listbox.insert(END, "Antonio    password")

        addButton = Button(top, text="add", command = lambda: self.editdialog(True))
        addButton.grid(row=0, column=0, padx=padx, pady=pady)

        editButton = Button(top, text="edit", command = lambda: self.editdialog(False))
        editButton.grid(row=0, column=1, padx=padx, pady=pady)

        removeButton = Button(top, text="remove", command= self.deletecollaborator)
        removeButton.grid(row=0, column=2, padx=padx, pady=pady)





    def fileedit(self):

        #TODO add something to make differ between new file and edit file
        #TODO get text from server
        padx = 2
        pady = 2

        top = Toplevel()
        top.title("File name here")

        closeallButton = Button(top, text="Close all")
        closeallButton.grid(row=0, column=0, padx=padx, pady=pady)

        closeclientButton = Button(top, text="Close client")
        closeclientButton.grid(row=0, column=1, padx=padx, pady=pady)

        managecollaboratorsButton = Button(top, text="Manage collaborators", command = self.managecollaborators)
        managecollaboratorsButton.grid(row=0, column=2, padx=padx, pady=pady)

        textField = Text(top)
        textField.grid(row=1, column=0, padx = padx, pady = pady)

        connectedcollabsLabel = Label(top, text = "Currently connected collabs")
        connectedcollabsLabel.grid(row=1, column=4, padx=padx, pady=pady)

    def initUI(self):


        padx = 2
        pady = 2

        self.newtextfileButton = Button(text = "New Text File", command = self.fileedit)
        self.newtextfileButton.grid(row = 0, column = 0, padx = padx, pady = pady)

        self.edityourfileButton = Button(text = "Edit your file", command = self.fileedit)
        self.edityourfileButton.grid(row = 1, column = 0, padx = padx, pady = pady)

        self.editelsefileButton = Button(text = "Edit outside file", command = self.connectdialog)
        self.editelsefileButton.grid(row = 0, column = 1, padx = padx, pady = pady)

        return True
