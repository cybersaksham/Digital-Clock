import datetime
from tkinter import *


class GUI(Tk):
    __hours = 0
    __minutes = 0
    __seconds = 0
    __timeNow = ""
    __dateNow = ""
    __zone = ""
    __stamps = 0

    def __init__(self, title, width, height, x_resizable, y_resizable):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(x_resizable, y_resizable)
        self.config(bg='black')

    def startWindow(self):
        self.__createList()
        self.__createLabel()
        self.__createBtn()
        self.__showTime()
        self.__printStamps()
        self.mainloop()

    def __createLabel(self):
        self.timeLabel = Label(self, text="", bg="black", fg="red", font="lucida 34 bold")
        self.timeLabel.pack()
        self.dateLabel = Label(self, text="", bg="black", fg="red", font="lucida 34 bold")
        self.dateLabel.pack()

    def __createList(self):
        self.listFrame = Frame(self)
        self.listFrame.pack(fill=X)
        self.headLabel = Label(self.listFrame, text="No.    Date       Time", anchor="w")
        self.headLabel.pack(fill=X)
        self.scroll = Scrollbar(self.listFrame)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.timeStamps = Listbox(self.listFrame, yscrollcommand=self.scroll.set)
        self.timeStamps.pack(fill=BOTH)
        self.scroll.config(command=self.timeStamps.yview)

    def __createBtn(self):
        self.btnWidget = Frame(self, bg="black")
        self.btnWidget.pack(fill=X)
        self.stampBtn = Button(self.btnWidget, text="Note", command=self.__makeStamp)
        self.stampBtn.grid(row=0, column=0, padx=100)
        self.clearBtn = Button(self.btnWidget, text="Reset", command=self.__resetStamps)
        self.clearBtn.grid(row=0, column=1, padx=100)

    def __formatTime(self):
        # Format Hour & Zone
        if self.__hours > 12:
            self.__hours -= 12
            self.__zone = "PM"
        elif self.__hours == 12:
            self.__zone = "PM"
        elif self.__hours == 0:
            self.__hours = 12
            self.__zone = "AM"
        else:
            self.__zone = "AM"

        # Format into 2 digits
        if self.__hours < 10:
            self.__hours = str(f"0{self.__hours}")
        if self.__minutes < 10:
            self.__minutes = str(f"0{self.__minutes}")
        if self.__seconds < 10:
            self.__seconds = str(f"0{self.__seconds}")

    def __getTime(self):
        self.timeObj = datetime.datetime.now()
        self.__hours = self.timeObj.hour
        self.__minutes = self.timeObj.minute
        self.__seconds = self.timeObj.second
        self.__dateNow = datetime.date.today().strftime("%d-%m-%y")

    def __showTime(self):
        self.__getTime()
        self.__formatTime()
        self.__timeNow = f"{self.__hours} : {self.__minutes} : {self.__seconds} {self.__zone}"
        self.timeLabel.config(text=self.__timeNow)
        self.dateLabel.config(text=f"{self.__dateNow}")
        self.dateLabel.after(500, self.__showTime)

    def __printStamps(self):
        f = open("stamps.txt", "r")
        lines = f.readlines()
        lines.reverse()
        self.__stamps = len(lines)
        for item in lines:
            self.timeStamps.insert(END, item[:-1])
        f.close()

    def __resetStamps(self):
        f = open("stamps.txt", "w")
        f.write("")
        self.__stamps = 0
        self.__clearStamp()
        f.close()

    def __makeStamp(self):
        self.__stamps += 1
        self.f = open("stamps.txt", "a")
        self.f.write(f"{self.__stamps}.   {self.__dateNow}   {self.__timeNow}\n")
        self.f.close()
        self.__clearStamp()
        self.__printStamps()

    def __clearStamp(self):
        self.timeStamps.delete(0, END)


if __name__ == '__main__':
    root = GUI("Digital Clock", 500, 335, 0, 0)
    root.startWindow()
