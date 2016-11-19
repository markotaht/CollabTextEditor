from Tkinter import *
from threading import Thread
from Commons import DEFAULT_PORT
from Util import differenceBetween

class ClientUI(Frame,Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        self.content = Tk()
        self.initUI()
        self.oldText = ""

    def run(self):
        self.content.mainloop()

    #Editing a remote file
    def remoteFile(self):
        padx = 2
        pady = 2

        top = Toplevel()
        top.title("Remote file + filename")

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
        #listbox.insert(END, "Antonio")


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
            #TODO check and connect
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

            if self.client.connect((ip,int(port)),usernameEntry.get(),passwordEntry.get()):
                window.destroy()
                self.remoteFile()
            else:
                print "ERROR, "*100

        connectButton = Button(top, text = "Connect", command=lambda: callback(top))
        connectButton.pack(side="bottom", padx=padx, pady=pady)
        connectButton.grid(row=3, column=1)

    #updates the collaborator list
    def updateCollaboratorsList(self, un, pw, addnew, window):

        if addnew:
            print "added", un, pw
            listbox.insert(END, un + "    " + pw)
            window.destroy()

        else:
            print "edited", listbox.get(ANCHOR) + "to", un, pw
            listbox.delete(ANCHOR)
            listbox.insert(END, un+"    "+pw)
            window.destroy()

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



        # TODO crashes when list is empty
        #workaround - check if there is something selected
        if listbox.get(ANCHOR)!= "":
            un = listbox.get(ANCHOR).split("    ")
            print "Editing", un
            usernameEntry.insert(0, un[0])
            passwordEntry.insert(0, un[1])


    def deleteCollaborator(self):

        un = listbox.get(ANCHOR)
        print "delete", un
        listbox.delete(ANCHOR)

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
        listbox.insert(END, "Antonio    password")

        addButton = Button(buttons, text="add", command = lambda: self.editCollaboratorsDialog(True))
        addButton.grid(row=0, column=0, padx=padx, pady=pady)

        editButton = Button(buttons, text="edit", command = lambda: self.editCollaboratorsDialog(False))
        editButton.grid(row=0, column=1, padx=padx, pady=pady)

        removeButton = Button(buttons, text="remove", command= self.deleteCollaborator)
        removeButton.grid(row=0, column=2, padx=padx, pady=pady)

    def closeClient(self):
        self.client.close()
        #TODO close ui


    #Sends local changes to be processed by client
    def changed(self, event):
        flag = textField.edit_modified()
        if flag:  # prevent from getting called twice
            print "Text changed locally"
            newText = textField.get("0.0", 'end-1c')
            #print "Old Text: ", self.oldText
            #print "New Text: ", newText
            index = differenceBetween(newText, self.oldText)
            self.client.processLocalChange(textField, self.oldText, newText, index[0], index[1], index[2])
            self.oldText = newText
        textField.edit_modified(False)

    #Mina kui host
    def fileedit(self):
        self.client.openLocally()
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

        manageCollaboratorsButton = Button(buttons, text="Manage collaborators", command = self.manageCollaborators)
        manageCollaboratorsButton.grid(row=0, column=2, padx=padx, pady=pady)


        global textField
        textField = Text(top)
        textField.grid(row=1, column=0, padx=padx, pady=pady)
        textField.bind('<<Modified>>', self.changed)
        textField.focus_set()

        self.client.textField = textField

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

        self.editelsefileButton = Button(text = "Edit outside file", command = self.connectDialog)
        self.editelsefileButton.grid(row = 0, column = 1, padx = padx, pady = pady)

        return True
