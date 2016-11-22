from Tkinter import *
from threading import Thread, Lock
from Commons import DEFAULT_PORT

class ClientUI(Frame,Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.lock = Lock()
        self.client = client
        self.content = Tk()
        self.initUI()
        self.oldText = ""
        self.textField = None
        self.collabbox = None
        self.sync = ""
        self.caretpos = 0

    def run(self):
        self.content.mainloop()

    def closeClient(self, host=False):
        print "safe close"
        self.content.destroy()
        self.client.close()
        if host:
            self.client.closeServer()

    def connectDialog(self):

        padx = 2
        pady = 2

        top = Toplevel()
        top.title("Connection Dialog")

        usernameLabel = Label(top, text = "Username:")
        usernameLabel.grid(row=0, column=0, padx=padx, pady=pady)

        usernameEntry = Entry(top)
        usernameEntry.grid(row=0, column=1, padx=padx, pady=pady)
        #TODO: Remove default placeholders later
        usernameEntry.insert(0, 'me')

        passwordLabel = Label(top, text = "Password:")
        passwordLabel.grid(row=1, column=0, padx=padx, pady=pady)

        passwordEntry = Entry(top, show = "*")
        passwordEntry.grid(row=1, column=1, padx=padx, pady=pady)
        # TODO: Remove default placeholders later
        passwordEntry.insert(0, 'admin')

        ipLabel = Label(top, text="IP & Port:")
        ipLabel.grid(row=2, column=0, padx=padx, pady=pady)

        ipEntry = Entry(top)
        ipEntry.grid(row=2, column=1, padx=padx, pady=pady)

        def callback(window):
            print usernameEntry.get()
            print passwordEntry.get()
            print ipEntry.get()

            if len(ipEntry.get()) == 0:
                #No ip specified
                ip = "127.0.0.1"
                port = str(DEFAULT_PORT)
            elif ":" not in ipEntry.get():
                #No port specified
                ip = ipEntry.get()
                port = str(DEFAULT_PORT)
            else:
                #Ip and port both specified
                ip,port = ipEntry.get().split(":")

            if self.client.connect((ip, int(port)), usernameEntry.get(), passwordEntry.get()):
                window.destroy()
                self.remoteFile()
            else:
                print "ERROR, "*100

        connectButton = Button(top, text = "Connect", command=lambda: callback(top))
        connectButton.pack(side="bottom", padx=padx, pady=pady)
        connectButton.grid(row=3, column=1)


    def updateCollaboratorsList(self, un, pw, addnew, window):
        # updates the collaborator list in manage collaborators
        if addnew:
            print "added", un, pw
            self.client.addCollaborator(un, pw)
            self.updatemanagecollaborators()
        #    self.updateOnlineCollaborators()
            window.destroy()


        else:
            print "edited", listbox.get(ANCHOR) +" " + "to", un, pw
            self.client.editCollaborator(listbox.get(ANCHOR).split("-")[0], un, pw)
            self.updatemanagecollaborators()
        #    self.updateOnlineCollaborators()
            window.destroy()

    def deleteCollaborator(self):
        #Deletes a collaborator from server
        un = listbox.get(ANCHOR)
        print "delete collaborator", un
        self.client.removeCollaborator(listbox.get(ANCHOR).split("-")[0])
        self.updatemanagecollaborators() #update managecollaborators
     #   self.updateOnlineCollaborators() #updates all collaborators (in main text edit window)


    def editCollaboratorsDialog(self, isAddingNew):
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

        doneButton = Button(top, text="done", command = lambda: self.updateCollaboratorsList(usernameEntry.get(), passwordEntry.get(), isAddingNew, top))
        doneButton.grid(row=2, column=1, padx=padx, pady=pady)


        #Make sure something is selected
        #otherwise close edit window
        if listbox.get(ANCHOR)  != "" and not isAddingNew:
            un = listbox.get(ANCHOR).split("-")
            print "Editing", un
            usernameEntry.insert(0, un[0])
            passwordEntry.insert(0, un[1])
        elif isAddingNew:
            pass
        else:
            top.destroy()


    def updatemanagecollaborators(self):
        #updates the collaborators list opened from "Manage collaborators"
        listbox.delete(0, END)
        for k, v in self.client.getCollaborators().iteritems():
            listbox.insert(END, str(k)+"-"+str(v))

    def updateOnlineCollaborators(self, online):
        online = online.split(",")
        try:
            self.collabbox.delete(0, END)
            for k in online:
                if len(k) != 0:
                    self.collabbox.insert(END, str(k))
        except AttributeError:
            pass#TODO here with remote text file

    def manageCollaborators(self):

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
        self.updatemanagecollaborators()


        addButton = Button(buttons, text="add", command = lambda: self.editCollaboratorsDialog(True))
        addButton.grid(row=0, column=0, padx=padx, pady=pady)

        editButton = Button(buttons, text="edit", command = lambda: self.editCollaboratorsDialog(False))
        editButton.grid(row=0, column=1, padx=padx, pady=pady)

        removeButton = Button(buttons, text="remove", command= self.deleteCollaborator)
        removeButton.grid(row=0, column=2, padx=padx, pady=pady)


    def left(self,event):
        self.client.moveCaret(-1)

    def right(self,event):
        self.client.moveCaret(1)

    #Sends local changes to be processed by client
    def changed(self, event):
        try:
            if ord(event.char) == 8:
                self.client.removeLetter()
            elif event.keysym == "Return":
                self.client.sendLetter("\n")
            else:
                self.client.sendLetter(event.char)
        except TypeError:
            print "noole klahv"

    def restorecaret(self, event):
        #moves caret to server's position. Used with up and down key and mouse1
        print "ingore and move caret to server position"
        self.textField.mark_set(INSERT, "1.0+%d chars" % self.caretpos)

    def common(self, top):
        padx = 2
        pady = 2
        self.textField = Text(top)
        self.textField.grid(row=1, column=0, padx=padx, pady=pady)
        self.textField.bind('<Key>', self.changed)
        self.textField.bind('<Left>', self.left)
        self.textField.bind('<Right>', self.right)

        # ignore and move caret to previous position
        self.textField.bind('<KeyRelease-Up>', self.restorecaret)
        self.textField.bind('<KeyRelease-Down>', self.restorecaret)
        self.textField.bind('<KeyRelease-Home>', self.restorecaret)
        self.textField.bind('<ButtonRelease-1>', self.restorecaret)
        self.textField.after(100, self.updateText)
        self.textField.focus_set()

        self.client.textField = self.textField

        buttons = LabelFrame(top, text="Currently connected collabs")
        buttons.grid(row=1, column=2, padx=padx, pady=padx)

        # create a listbox and populate it
        self.collabbox = Listbox(buttons)
        self.collabbox.grid(row=0, column=0, padx=padx, pady=pady)

        self.updateOnlineCollaborators("")


    #Mina kui host
    def fileedit(self, filename):
        self.client.openLocally(filename)

        padx = 2
        pady = 2

        top = Toplevel()
        top.title(filename)

        buttons = LabelFrame(top)
        buttons.grid(row=0, column=0, padx=padx, pady=pady)

        closeclientButton = Button(buttons, text="Close", command =lambda: self.closeClient(True))
        closeclientButton.grid(row=0, column=1, padx=padx, pady=pady)

        manageCollaboratorsButton = Button(buttons, text="Manage collaborators", command = self.manageCollaborators)
        manageCollaboratorsButton.grid(row=0, column=2, padx=padx, pady=pady)

        # handles close from 'X'
        top.protocol('WM_DELETE_WINDOW', lambda: self.closeClient(True))

        self.common(top)

    # Editing a remote file
    def remoteFile(self):
        padx = 2
        pady = 2

        top = Toplevel()
        top.title("Remote file")

        disconnectButton = Button(top, text="Disconnect", command=self.closeClient)
        disconnectButton.grid(row=0, column=0, padx=padx, pady=pady)

        # handles close from 'X'
        top.protocol('WM_DELETE_WINDOW', lambda: self.closeClient(False))

        self.common(top)


    def ignore(self,event):
        return "break"

    def updateText(self):
        #updates textfield with text from server
        #sets caret pos to what it is in the server
        #updates self.caretpos to servers value - used with up and down arrow events

        content,caret, online = self.client._synchronise([])
        if content == "CLOSE":
            self.closeClient()
            return

        if (self.textField != None) and self.sync != content:
            self.sync = content
            try:
                self.textField.delete("1.0", END)
            except:
                pass
            self.textField.insert("1.0", content)
            self.textField.mark_set("insert","1.0+%d chars" % caret)
            self.caretpos = caret

        #mark people who are online
        self.updateOnlineCollaborators(online)
        self.textField.after(100, self.updateText)

    def getText(self):
        return self.sync

    def filenamedialog(self):
        #dialog after pressing "Local file"
        #asks for filename, does not accept empty name

        padx = 2
        pady = 2

        top = Toplevel()
        top.title("Enter file name")

        def callback():
            filename = self.filenameentry.get()
            if filename != "":
                top.destroy()
                self.fileedit(filename)

        self.filenamelabel = Label(top, text="Enter file name (no extension):")
        self.filenamelabel.grid(row=0, column=0, padx=padx, pady=pady)

        self.filenameentry = Entry(top)
        self.filenameentry.grid(row=1, column=0, padx=padx, pady=pady)

        self.okbutton = Button(top, text = "Ok", command=callback)
        self.okbutton.grid(row=2, column=0, padx=padx, pady=pady)

        self.filenameentry.focus_set()


    def initUI(self):

        padx = 2
        pady = 2

        self.content.title("Googol Docs")


        self.edityourfileButton = Button(text = "Local file", command = self.filenamedialog)
        self.edityourfileButton.grid(row = 0, column = 0, padx = padx, pady = pady)

        self.editelsefileButton = Button(text = "Remote file", command = self.connectDialog)
        self.editelsefileButton.grid(row = 0, column = 1, padx = padx, pady = pady)

        return True

