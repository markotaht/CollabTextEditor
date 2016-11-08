import Tkinter

class ClienUI:
    def __init__(self, client):
        self.client = client
        self.content = Tkinter.Tk()
        self.initUI()

    def run(self):
        self.content.mainloop()
        print "YAY"

    def initUI(self):
        return True