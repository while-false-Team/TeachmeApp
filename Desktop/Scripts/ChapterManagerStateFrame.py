import customtkinter as tk
from TopicDataModule import *
import global_variables

class ChapterDataStateFrame:
    def __init__(self, master:tk.CTkFrame, topicManager:TopicManager, go_to_test, go_to_learn, go_to_edit, refresh, index:int) -> None:
        self.frame = master
        self.topicData = topicManager
        self.index = index
        self.topicData.initFor(index)
        self.go_to_test = go_to_test
        self.go_to_learn = go_to_learn
        self.go_to_edit = go_to_edit
        self.refreshState = refresh
        if len(self.topicData.topicsData) > 0:
            self.currentDataId = self.topicData.topicsData[0].id
            self.initVariables()
            self.initWidgets()
            self.initPacks()
        else:
            self.initForEmptyTopics()

    def initForEmptyTopics(self):
        
        self.emptyLabel = tk.CTkLabel(self.frame, text="Nie masz tu jeszcze żadnych tematów", font=("Play", 20))
        if self.index==1:
            self.emptyLabel.configure(height=183)
            self.emptyLabel.pack(fill=tk.X,expand=True,anchor=tk.CENTER)
            self.firstButton = tk.CTkButton(self.frame, text="Dodaj pierwszy temat", anchor="center", command=self.newChapter)
            self.firstButton.pack(expand=True,anchor=tk.CENTER,pady=(0,120))
        elif self.index==2:
            if global_variables.id_class==None:
                self.emptyLabel.configure(text="Wpisz kod klasy, aby do niej dołączyć")
                self.emptyLabel.pack(fill=tk.X,expand=True,anchor=tk.N,pady=(80,10))
                self.codeEntry = tk.CTkEntry(self.frame,width=140,font=("Play", 20),justify=tk.CENTER)
                self.codeEntry.pack(expand=True,anchor=tk.CENTER,pady=13,ipady=5)
                self.codeEntry.bind('<Return>',self.checkCode)
                self.okButton = tk.CTkButton(self.frame, text="Zatwierdź", anchor="center", command=self.checkCode)
                self.okButton.pack(expand=True,anchor=tk.S,pady=(0,90))
                self.annoucement_var = tk.StringVar(value="")
                tk.CTkLabel(self.frame, textvariable=self.annoucement_var).pack()
            else:
                query = f"SELECT nazwa_klasy FROM klasy WHERE id_klasy={global_variables.id_class}"
                global_variables.mycursor.execute(query)
                row=global_variables.mycursor.fetchall()
                self.emptyLabel2 = tk.CTkLabel(self.frame, textvariable=tk.StringVar(value=f"Klasa: \"{row[0][0]}\" nie ma jeszcze tematów"), font=("Play", 20),height=330)
                self.emptyLabel2.pack(fill=tk.X,expand=True,anchor=tk.CENTER)
        else:
            self.emptyLabel.configure(height=330)
            self.emptyLabel.pack(fill=tk.X,expand=True,anchor=tk.CENTER)

    def checkCode(self, event=""):
        query = f"SELECT id_klasy FROM klasy WHERE kod_klasy='{self.codeEntry.get()}'"
        global_variables.mycursor.execute(query)

        result = global_variables.mycursor.fetchall()
        if len(result) == 0:
            self.annoucement_var.set("Klasa o takim kodzie, nie istnieje!")
        else:
            query = f"UPDATE `uczniowie` SET `id_klasy`={result[0][0]} WHERE id_ucznia={self.topicData.user_id};"
            global_variables.mycursor.execute(query)
            global_variables.mydb.commit()
            global_variables.id_class = result[0][0]
            self.refreshState()
            



    def initVariables(self):
        pass
    def initWidgets(self):
        self.secondframe = tk.CTkFrame(self.frame)
        self.secondframe.columnconfigure(0, weight=1)
        self.secondframe.columnconfigure(1, weight=1)
        self.topicScrollBar = tk.CTkScrollableFrame(self.secondframe, width=150, height=290, bg_color="#292929")
        self.newButtonFrame = tk.CTkFrame(self.secondframe, height=30, bg_color="#292929")
        self.newButton = tk.CTkButton(self.newButtonFrame, text="Nowy temat", anchor="center", state='disabled', command=self.newChapter)
        if self.index == 1:
            self.newButton.configure(state='normal')

    def initPacks(self):
        self.secondframe.pack(anchor=tk.W, fill=tk.X)
        self.initScrollBar()
        self.topicScrollBar.grid(row=0, column=0, sticky=tk.N+tk.E+tk.W)
        self.newButtonFrame.grid(row=0, column=0,sticky=tk.S)
        self.fourthFrame.grid(row=0,column=1, sticky=tk.S+tk.N+tk.W+tk.E)
        self.thirdframe.grid(row=0, column = 1, sticky=tk.NW)
        self.newButton.pack(padx=18)

    def initScrollBar(self):      
        self.labelsvalues = [
            tk.StringVar(value=self.topicData.topicsData[0].name),
            tk.StringVar(value=self.topicData.topicsData[0].finished_counter),
            tk.StringVar(value=self.topicData.topicsData[0].date),
            tk.StringVar(value=str("Poziom przyswojenia:  "+self.topicData.topicsData[0].acquistion_level)),
            tk.StringVar(value=""),
            tk.StringVar(value="")
        ]
        self.fourthFrame = tk.CTkFrame(self.secondframe, height=330, bg_color="#292929")
        self.thirdframe = tk.CTkFrame(self.secondframe, bg_color="#292929")
        self.topicLabel = tk.CTkLabel(self.thirdframe, text="Nazwa",font=("Play",17), anchor="center", bg_color="#1f538d").grid(row=0, column=0, ipadx=10, pady=10, sticky="wens")
        self.finishedLabel = tk.CTkLabel(self.thirdframe, text="Ile ukończeń", font=("Play",17), anchor="center", bg_color="#1f538d").grid(row=0, column=1, ipadx=10, pady=10, sticky="wens")
        self.dateLabel = tk.CTkLabel(self.thirdframe, text="Ukończono",font=("Play",17), anchor="center", bg_color="#1f538d").grid(row=0, column=2, ipadx=10, pady=10, sticky="wens")

        self.topicLabel = tk.CTkLabel(self.thirdframe, textvariable=self.labelsvalues[0],font=("Play",16, "bold"), anchor="center").grid(row=1, column=0, ipadx=10, ipady=10, sticky="wens")
        self.finishedLabel = tk.CTkLabel(self.thirdframe, textvariable=self.labelsvalues[1], font=("Play",15, "italic"), anchor="center").grid(row=1, column=1, ipadx=10, ipady=10, sticky="wens")
        self.dateLabel = tk.CTkLabel(self.thirdframe, textvariable=self.labelsvalues[2],font=("Play",15, "italic"), anchor="center").grid(row=1, column=2, ipadx=10, ipady=10, sticky="wens")

        fun = lambda : self.go_to_edit(self.currentDataId, self.topicData.get_data_on_id(self.currentDataId).name)
        self.editButton = tk.CTkButton(self.thirdframe, text="Edytuj", anchor="center", state='disabled', command=fun)
        if self.index == 1:
            self.editButton.configure(state='normal')
        self.editButton.grid(row=2, column=0,pady=(10,5))
        fun = lambda : self.go_to_learn(self.currentDataId)
        self.learnButton = tk.CTkButton(self.thirdframe, text="Nauka", anchor="center", command=fun)
        self.learnButton.grid(row=2, column=1, padx=2, pady=(10,5))
        fun = lambda : self.go_to_test(self.currentDataId)
        self.testButton = tk.CTkButton(self.thirdframe, text="Test", anchor="center", command=fun)
        self.testButton.grid(row=2, column=2, pady=(10,5))
        self.levelLabel1 = tk.CTkLabel(self.thirdframe, textvariable=self.labelsvalues[3], font=("Play",15)).grid(row=3, column=0, columnspan=2, pady=10,sticky=tk.W, padx=10)
        self.emptyLabel2 = tk.CTkLabel(self.thirdframe, textvariable=self.labelsvalues[4],font=("Play",15)).grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=10)
        for data in self.topicData.topicsData:
            fun = lambda data=data: self.konstructButton(data) 
            button = tk.CTkButton(self.topicScrollBar, text=data.name, font=("Play",15), command=fun, width=200)
            button.pack(pady=2)

    def konstructButton(self, data:TopicData):
        self.currentDataId = data.id
        self.labelsvalues[0].set(data.name)
        self.labelsvalues[1].set(data.finished_counter)            
        self.labelsvalues[2].set(data.date)
        self.labelsvalues[3].set("Poziom przyswojenia:  "+data.acquistion_level)
        if data.zeroWords():
            self.labelsvalues[4].set("Ten temat jest pusty!")
            self.learnButton.configure(state="disabled")
            self.testButton.configure(state="disabled")
        else:
            self.labelsvalues[4].set("")
            self.learnButton.configure(state="normal")
            self.testButton.configure(state="normal")

    def refresh(self):
        self.topicData.initFor(self.index)

    def getCurrentTopicId(self):
        return self.currentDataId

    def newChapter(self):
        if self.index == 0:
            query = f"INSERT INTO `tematy`(`nazwa_tematu`) VALUES ('Nowy temat')"
        elif self.index == 1:
            query = f"INSERT INTO `tematy`(`nazwa_tematu`,`id_ucznia`) VALUES ('Nowy temat',{self.topicData.user_id})"
        elif self.index == 2:
            query = f"INSERT INTO `tematy`(`nazwa_tematu`,`id_klasy`) VALUES ('Nowy temat', {self.topicData.class_id});"
        global_variables.mycursor.execute(query)
        global_variables.mydb.commit()
        self.refresh()
        data = self.topicData.topicsData[len(self.topicData.topicsData)-1]
        self.go_to_edit(data.id, data.name)
