from Tkinter import *
from threading import Thread


#TODO move to commons
def difference(s1, s2):
    if len(s1) == len(s2):
        return [i for i in xrange(len(s2)) if s1[i] != s2[i]][0]
    #this detects additions
    elif len(s1) > len(s2):
        # check if we added into the middle or into the end
        index = [i for i in xrange(len(s2)) if s1[i] != s2[i]]
        if len(index) == 0:
            return ("+", len(s1) - 1, s1[-1])
        else:
            print "right", index
            return ("+", index[0], s1[index[0]])
    #this detects removals
    else:
        # check if we added into the middle or into the end
        index = [i for i in xrange(len(s1)) if s1[i] != s2[i]]
        if len(index) == 0:
            return ("-",(len(s2) - 1), s2[-1])
        else:
            return ("-",index[0], s2[index[0]])


class ClienUI(Frame,Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        self.content = Tk()
        self.initUI()
        self.previoustext = ""

    def run(self):
        self.content.mainloop()

    def outsidefile(self):
        padx = 2
        pady = 2

        top = Toplevel()
        top.title("Outside file + filename")

        disconnectButton = Button(top, text="Disconnect")
        disconnectButton.grid(row=0, column=0, padx=padx, pady=pady)

        global textField
        textField = Text(top)
        textField.grid(row=1, column=0, padx=padx, pady=pady)
        textField.bind('<<Modified>>', self.changed)
        textField.focus_set()

        connectedcollabsFrame = LabelFrame(top, text="Currently connected collabs")
        connectedcollabsFrame.grid(row=1, column=1, padx=padx, pady=padx)

        listbox = Listbox(connectedcollabsFrame)
        listbox.grid(row=0, column=0, padx=padx, pady=pady)
        listbox.insert(END, "Antonio")


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

        def callback(window):
            #TODO check and connect
            print usernameEntry.get()
            print passwordEntry.get()
            print ipEntry.get()
            ip,port = ipEntry.get().split(":")
            if self.client.connect((ip,int(port))):
                window.destroy()
                self.outsidefile()
            else:
                print "ERROR, "*100

        connectButton = Button(top, text = "Connect", command=lambda: callback(top))
        connectButton.pack(side="bottom", padx=padx, pady=pady)
        connectButton.grid(row=3, column=1)

    #updates the collaborator list
    def updatelist(self, un, pw, addnew, window):

        if addnew:
            print "added", un, pw
            listbox.insert(END, un + "    " + pw)
            window.destroy()

        else:
            print "edited", listbox.get(ANCHOR) + "to", un, pw
            listbox.delete(ANCHOR)
            listbox.insert(END, un+"    "+pw)
            window.destroy()

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

        cancelButton = Button(top, text="cancel", command = top.destroy)
        cancelButton.grid(row=2, column=0, padx=padx, pady=pady)

        doneButton = Button(top, text="done", command = lambda: self.updatelist(usernameEntry.get(), passwordEntry.get(), isAddingnew, top))
        doneButton.grid(row=2, column=1, padx=padx, pady=pady)



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

        global listbox

        buttons = LabelFrame(top)
        buttons.grid(row=0, column=0,padx=10, pady=10)

        list = LabelFrame(top, text = "Username password",padx=padx, pady=pady)
        list.grid(row=1, column=0, padx=padx, pady=pady)

        listbox = Listbox(list)
        listbox.grid(row=2, column=0, padx=padx, pady=pady)
        listbox.insert(END, "Antonio    password")

        addButton = Button(buttons, text="add", command = lambda: self.editdialog(True))
        addButton.grid(row=0, column=0, padx=padx, pady=pady)

        editButton = Button(buttons, text="edit", command = lambda: self.editdialog(False))
        editButton.grid(row=0, column=1, padx=padx, pady=pady)

        removeButton = Button(buttons, text="remove", command= self.deletecollaborator)
        removeButton.grid(row=0, column=2, padx=padx, pady=pady)

    def closeClient(self):
        self.client.close()
        #TODO close ui



    #pushes changes if letters are added or deleted
    #TODO get previoustext from server

    def changed(self, event):
        flag = textField.edit_modified()
        if flag:  # prevent from getting called twice
            print "changed called"
            text = textField.get("0.0", 'end-1c')
            print "text was", text
            print "previous was", self.previoustext
            index = difference(text, self.previoustext)
            print "change was", index
            if index[0] == "+":
                self.client.sendLetter(index[2], index[1])
            else:
                self.client.removeLetter(index[1])
            self.previoustext = text
        textField.edit_modified(False)


    def fileedit(self):

        #TODO add something to make differ between new file and edit file
        #TODO get text from server
        padx = 2
        pady = 2

        top = Toplevel()
        top.title("File name here")

        buttons = LabelFrame(top)
        buttons.grid(row=0, column=0, padx=padx, pady=pady)


        closeallButton = Button(buttons, text="Close all")
        closeallButton.grid(row=0, column=0, padx=padx, pady=pady)

        closeclientButton = Button(buttons, text="Close client", command = self.closeClient)
        closeclientButton.grid(row=0, column=1, padx=padx, pady=pady)

        managecollaboratorsButton = Button(buttons, text="Manage collaborators", command = self.managecollaborators)
        managecollaboratorsButton.grid(row=0, column=2, padx=padx, pady=pady)


        global textField
        textField = Text(top)
        textField.grid(row=1, column=0, padx=padx, pady=pady)
        textField.bind('<<Modified>>', self.changed)
        textField.focus_set()



        buttons = LabelFrame(top, text="Currently connected collabs")
        buttons.grid(row=1, column=2, padx=padx, pady=padx)

        listbox = Listbox(buttons)
        listbox.grid(row=0, column=0, padx=padx, pady=pady)
        listbox.insert(END, "Antonio")

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
