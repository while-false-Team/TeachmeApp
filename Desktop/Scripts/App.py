import customtkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
from StateManager import *
from WordsModule import *
from Summary import SummaryTable
from TopicDataModule import *
from ChapterManagerStateFrame import ChapterDataStateFrame
from AutoLogin import AutoLogin
from TeacherManagerStateFrame import *
import global_variables
from argon2 import PasswordHasher
from googletrans import Translator


class ChapterMenuState(State):
    def __init__(self, master: tk.CTk, state_manager:State_Manager) -> None:
        super().__init__(master, state_manager)
        self.initVariables()
        self.initWidgets()
        self.initPacks()

    def initVariables(self):
        self.tabs = tk.CTkTabview(self.frame)
        self.tabs.add("Tematy ogólne")
        self.tabs.add("Tematy prywatne")
        self.tabs.add("Klasy")
    def initWidgets(self):
        self.title_label = tk.CTkLabel(self.frame, text="Tematy", font=("Play",30,"bold"),bg_color="#1f538d")
        ChapterDataStateFrame(self.tabs.tab("Tematy ogólne"), TopicManager(user_id=global_variables.id_user, class_id=global_variables.id_class), self.go_to_test,self.go_to_learn, self.go_to_edit,self.refresh, 0)
        ChapterDataStateFrame(self.tabs.tab("Tematy prywatne"), TopicManager(user_id=global_variables.id_user, class_id=global_variables.id_class),self.go_to_test,self.go_to_learn, self.go_to_edit,self.refresh, 1)
        ChapterDataStateFrame(self.tabs.tab("Klasy"), TopicManager(user_id=global_variables.id_user, class_id=global_variables.id_class),self.go_to_test,self.go_to_learn, self.go_to_edit,self.refresh, 2)
        self.logout_button = tk.CTkButton(self.frame, text="Wyloguj", command=self.logout_fun)
    def initPacks(self):
        self.packFrame()
        self.title_label.pack(ipady=9, fill=tk.X, anchor=tk.N)
        self.tabs.pack(anchor=tk.N,fill=tk.X)
        self.logout_button.pack(anchor=tk.S, expand=True,pady=(0,10))

    def refresh(self):
        self.pushNewDelCur(ChapterMenuState(self.frame.master, self.state_manager_ptr))

    def go_to_test(self, currentDataId):self.pushNewDelCur(MainState(self.frame.master, self.state_manager_ptr, currentDataId))

    def go_to_learn(self, currentDataId):self.pushNewDelCur(LernState(self.frame.master, self.state_manager_ptr, currentDataId))

    def logout_fun(self):
        global global_variables
        global_variables.id_user=0
        global_variables.id_class=0
        AutoLogin.del_current_data()
        self.pushNewDelCur(LoginState(self.frame.master, self.state_manager_ptr))

    def go_to_edit(self, currentDataId:int, topic_name:str):self.pushNewDelCur(EditorState(self.frame.master, self.state_manager_ptr, currentDataId, topic_name))




class MainState(State):
    def __init__(self, master: tk.CTk, state_manager:State_Manager, topic_id:int) -> None:
        super().__init__(master, state_manager)
        self.topic_id = topic_id
        self.initVariables()
        self.initWidgets()
        self.initPacks()

    def initVariables(self):
        self.chapter = Words(self.topic_id)
        self.chapter_name= tk.StringVar(value=self.chapter.chapter_name)
        self.steps=len(self.chapter.wordsList)*self.chapter.neededPoints
        self.currentStep = 0.0        
        self.was_helped = False
        self.addPoints = True
        self.currentLetter = 0
    def initWidgets(self):
        self.title_label = tk.CTkLabel(self.frame, textvariable=self.chapter_name, font=("Play",30,"bold"),bg_color="#1f538d")
        self.progressbar = tk.CTkProgressBar(self.frame,width=450)
        self.progressbar.set(self.currentStep)
        self.ex_label = tk.CTkLabel(self.frame, text="Przetłumacz poniższe słowo", font=("Play",15,"italic"))
        self.word_var = tk.StringVar(value=self.chapter.getWord())
        self.word_frame=tk.CTkFrame(self.frame)
        self.word = tk.CTkLabel(self.word_frame, textvariable=self.word_var, font=("Play",15,"bold"))
        self.entry = tk.CTkEntry(self.frame)
        self.entry.focus()
        self.entry.bind('<Return>', self.check_button_fun)
        self.annoucement_var = tk.StringVar()
        self.annoucement = tk.CTkLabel(self.frame, textvariable=self.annoucement_var)
        self.check_button = tk.CTkButton(self.frame, text="Zatwierdź", command=self.check_button_fun)
        self.letter_button = tk.CTkButton(self.frame, text="Litera", command=self.letter_button_fun)
        self.menu_button = tk.CTkButton(self.frame, text="Powrót", command=self.go_back)
    def initPacks(self):
        self.packFrame()
        self.title_label.pack(ipady=9, fill=tk.X, anchor=tk.N)
        self.progressbar.pack(pady=10)
        self.ex_label.pack(ipady=20)
        self.word_frame.pack(ipadx=10)
        self.word.pack()
        self.entry.pack(pady=10)
        self.annoucement.pack()
        self.check_button.pack()
        self.letter_button.pack(pady=5)
        self.menu_button.pack(anchor=tk.SE, expand=True)

    def letter_button_fun(self,event=""):
        self.was_helped=True
        self.addPoints=False
        self.entryLen=len(self.entry.get())
        if self.entryLen > len(self.chapter.getTranslation()):
            self.annoucement_var.set("Za długie słowo")
        else:
            i=0
            for letter in self.entry.get():
                if letter.lower() == str(self.chapter.getTranslation()[i]).lower():
                    i+=1
                else:
                    eaog=self.entry.get()[0:i]+self.chapter.getTranslation()[i:i+1]
                    self.entry.delete(0, tk.END)
                    self.entry.insert(0, eaog)
                    self.annoucement_var.set("Dodano literę")
                    break
            if i==len(self.chapter.getTranslation()):
                self.annoucement_var.set("To już wszystko")
            else:
                eaog=self.entry.get()[0:i]+self.chapter.getTranslation()[i:i+1]
                self.entry.delete(0, tk.END)
                self.entry.insert(0, eaog)
                self.annoucement_var.set("Dodano literę")

    def check_button_fun(self, event=""):
        if self.entry.get() != "" and self.entry.get()[0] != " ":
            if self.chapter.checkCorrectness(self.entry.get().lower(),self.addPoints) and not self.chapter.is_end:
                if self.was_helped == True:
                    self.currentLetter=0
                    self.was_helped=False
                else:
                    self.currentStep+=1/self.steps
                self.annoucement_var.set("")
                self.word_var.set(self.chapter.getWord())
                self.entry.delete(0, tk.END)
                self.addPoints=True
            elif self.chapter.is_end:
                self.dataBaseUpdate()
                self.pushNewDelCur(EndState(self.frame.master, self.state_manager_ptr, self.chapter))
            else:
                self.addPoints=False
                self.punkty=self.chapter.wordsList[self.chapter.current_index].points
                if self.punkty>0:
                    self.currentStep-=self.punkty*(1/self.steps)
                self.chapter.clearPoints()
                self.annoucement_var.set("Błędna odpowiedź")
                self.word_var.set(self.chapter.getWord() + " -> " + self.chapter.getTranslation())
                self.entry.delete(0, tk.END)
                self.entry.configure(state=tk.DISABLED)
                self.was_helped=True
                self.frame.after(2000, self.clear_hint)
            self.progressbar.set(self.currentStep)
        else:
            self.annoucement_var.set("Puste pole, wprowadź wartość")

    def entryFocus(self):self.entry.focus()

    def dataBaseUpdate(self):
        query = f"UPDATE `dane_tematow` SET `ile_ukonczen`= ile_ukonczen+1, `data_ostatniego_uruchomienia`=CURRENT_DATE(), `poziom_przyswojenia`='{self.chapter.get_acquistion_level()}' WHERE id_ucznia = {global_variables.id_user} AND id_tematu = {self.chapter.chapter_id};"
        global_variables.mycursor.execute(query)
        global_variables.mydb.commit()

    def clear_hint(self):
        self.word_var.set(self.chapter.getWord())
        self.entry.configure(state=tk.NORMAL)

    def go_back(self):self.pushNewDelCur(ChapterMenuState(self.frame.master, self.state_manager_ptr))



class EndState(State):
    def __init__(self, master: tk.CTk, state_manager:State_Manager, words:Words) -> None:
        super().__init__(master, state_manager)
        self.words = words
        self.initVariables()
        self.initWidgets()
        self.initPacks()

    def initVariables(self):...
    def initWidgets(self):
        self.title_label = tk.CTkLabel(self.frame, text="Podsumowanie", font=("Play",30,"bold"),bg_color="#1f538d")
        self.menu_button = tk.CTkButton(self.frame, text="Powrót", command=self.go_back)
    def initPacks(self):
        self.packFrame()
        self.title_label.pack(ipady=9, fill=tk.X, anchor=tk.N)
        self.summary_table = SummaryTable(self.frame, self.words)
        self.menu_button.pack(anchor=tk.SE, expand=True)
    
    def go_back(self):self.pushNewDelCur(ChapterMenuState(self.frame.master, self.state_manager_ptr))


class EditorState(State):
    def __init__(self, master: tk.CTk, state_manager, topic_id, topic_name, class_data=None) -> None:
        super().__init__(master, state_manager)
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.class_data = class_data
        self.translator = Translator()
        #Zmienne 
        self.title_entry_var = tk.StringVar(value=self.topic_name)
        self.words_manager = WordsEditor(self.topic_id)
        self.annoucement_var = tk.StringVar()
        self.entrys = list()
        
        #Widgety
        self.title_entry = tk.CTkEntry(self.frame, textvariable=self.title_entry_var, font=("Play", 30, "bold"),bg_color="#1f538d")
        self.buttons_frame = tk.CTkFrame(self.frame, width=450, height=30)
        self.annoucement = tk.CTkLabel(self.buttons_frame, textvariable=self.annoucement_var)
        add_new_word = tk.CTkButton(self.buttons_frame, text="Dodaj słówko", command=self.add_new_word)
        save_words = tk.CTkButton(self.buttons_frame, text="Zapisz słówka", command=self.save)
        delete_topic = tk.CTkButton(self.buttons_frame, text="Usuń temat", command=self.delete_topic)
        menu_button = tk.CTkButton(self.frame, text="Powrót", command=self.go_back)
        self.edit_frame = tk.CTkScrollableFrame(self.frame, width=450, height=300)
        
        iterator = 0
        for word in self.words_manager.words:
            entry1 = tk.CTkEntry(self.edit_frame, textvariable=tk.StringVar(value=word.word))
            fun = lambda event="",index=iterator: self.translate(index)
            entry1.bind("<Tab>", fun)
            entry2 = tk.CTkEntry(self.edit_frame, textvariable=tk.StringVar(value=word.translation))
            fun = lambda index = iterator: self.konstruct_delete_button(index)
            delete_button = tk.CTkButton(self.edit_frame, text="Usuń", command=fun)
            self.entrys.append([entry1, entry2, delete_button])
            iterator+=1

        #Pakowanie widgetów
        self.packFrame()
        self.title_entry.pack(ipady=9, fill=tk.X, anchor=tk.N)
        self.edit_frame.pack()
        self.buttons_frame.pack(expand=True)
        self.annoucement.grid(row=0, column=0,columnspan=3)
        add_new_word.grid(row=1, column=1, sticky=tk.W+tk.N+tk.S+tk.E, padx=8, pady=(0, 23))
        save_words.grid(row=1, column=0, sticky=tk.W+tk.N+tk.S+tk.E, padx=10, pady=(0, 23))
        delete_topic.grid(row=1, column=2, sticky=tk.W+tk.N+tk.S+tk.E, padx=8, pady=(0, 23))
        menu_button.pack(anchor=tk.SE, expand=True)
        row = 0
        for entry in self.entrys:
            entry[0].grid(row=row, column=0, pady=3)
            entry[1].grid(row=row, column=1, pady=3)
            entry[2].grid(row=row, column=2, pady=3)
            row+=1
        self.add_new_word()
        
    def add_new_word(self, event=""):
            if len(self.entrys)>0:
                self.entrys[-1][0].unbind("<Tab>")
            new_entry1 = tk.CTkEntry(self.edit_frame, textvariable=tk.StringVar())
            fun = lambda event="", index=len(self.entrys): self.translate(index)
            new_entry1.bind("<Tab>", fun)
            new_entry2 = tk.CTkEntry(self.edit_frame, textvariable=tk.StringVar())
            fun = lambda index=len(self.entrys): self.konstruct_delete_button(index)
            delete_button = tk.CTkButton(self.edit_frame, text="Usuń", command=fun)
            self.entrys.append([new_entry1, new_entry2, delete_button])
            self.entrys[-1][0].grid(row=len(self.entrys), column=0,pady=3)
            self.entrys[-1][1].grid(row=len(self.entrys), column=1,pady=3)
            self.entrys[-1][2].grid(row=len(self.entrys), column=2,pady=3)
            self.words_manager.add_new_word("","")
            self.entrys[-1][0].bind("<Tab>", self.add_new_word)

    def konstruct_delete_button(self, index):
        self.words_manager.words[index].to_delete = True
        if len(self.entrys)>1:
            self.entrys[-1][0].unbind("<Tab>")
            for i in range(index, len(self.entrys)-1):
                self.entrys[i][0].delete(0, tk.END)
                self.entrys[i][1].delete(0, tk.END)
                self.entrys[i][0].insert(0, self.entrys[i+1][0].get())
                self.entrys[i][1].insert(0, self.entrys[i+1][1].get())

            self.words_manager.pop_word(index)

            self.entrys[-1][0].destroy()
            self.entrys[-1][1].destroy()
            self.entrys[-1][2].destroy()
            self.entrys.pop(-1)
            self.entrys[-1][0].bind("<Tab>", self.add_new_word)
        elif len(self.entrys)==1:
            self.words_manager.pop_word(index)
            self.entrys[-1][0].destroy()
            self.entrys[-1][1].destroy()
            self.entrys[-1][2].destroy()
            self.entrys.pop(-1)

    def save(self):
        if len(self.entrys)>=1:
            if len(self.title_entry.get()) > 15:
                self.annoucement_var.set("Nazwa tematu jest zbyt długa!(max 15 znaków)")
                return 0
            while self.entrys[-1][0].get() == "" and self.entrys[-1][1].get() == "":
                    self.entrys[-1][0].destroy()
                    self.entrys[-1][1].destroy()
                    self.entrys[-1][2].destroy()
                    self.entrys.pop(-1)
                    self.words_manager.pop_word(-1)
            for val in self.entrys:
                word = val[0].get()
                translation = val[1].get()
                try:
                    if word == '' or translation == '' or word[0]==" " or translation[0]==" ":
                        self.annoucement_var.set("Nie wszystkie pola są wypełnione!")
                        return 0
                except IndexError:
                    self.annoucement_var.set("Nie wszystkie pola są wypełnione!")
                    return 0
            else:
                self.annoucement_var.set("")

            for i in range(0, len(self.entrys)):
                self.words_manager.words[i].word = self.entrys[i][0].get()
                self.words_manager.words[i].translation = self.entrys[i][1].get()      
            try:
                self.words_manager.save_to_database()
                self.words_manager.update_title(self.title_entry.get())
                self.go_back()
            except:
                self.annoucement_var.set("Użyto niedozwolonych zanaków specjalnych!")
        else:
            self.delete_topic()

    def delete_topic(self):
        if messagebox.askyesno("Jesteś pewien?", "Czy napewno chcesz usunąć ten temat?\nZmiany będą nieodwracalne!"):
            self.words_manager.delete_topic()
            self.go_back()


    def go_back(self):
        if global_variables.isTeacher:self.pushNewDelCur(ChapterManager(self.frame.master, self.state_manager_ptr, self.class_data))
        else:self.pushNewDelCur(ChapterMenuState(self.frame.master, self.state_manager_ptr))

    def translate(self, index):
        if len(self.entrys[index][0].get()) ==0: return 0
        dest=""
        if self.translator.detect(self.entrys[index][0].get()).lang == 'pl':
            dest='en'
        elif self.translator.detect(self.entrys[index][0].get()).lang == 'en':
            dest='pl'
        else: return 0
        if len(self.entrys[index][1].get())==0: self.entrys[index][1].insert(index=0,string=self.translator.translate(self.entrys[index][0].get(), dest).text.capitalize())




class LernState(State):
    def __init__(self, master: tk.CTk, state_manager,topic_id:int) -> None:
        super().__init__(master, state_manager)
        self.topic_id = topic_id
        self.initVariables()
        self.initWidgets()
        self.initPacks()

    def initVariables(self):
        self.chapter = Words(self.topic_id)
        self.chapter.setZeroAsCurrentIndex()
        self.chapter_name= tk.StringVar(value=self.chapter.chapter_name)
        self.steps=len(self.chapter.wordsList)
        self.count_var = tk.StringVar(value=("1 / "+str(self.steps)))
        self.word_var = tk.StringVar(value=(self.chapter.getWord()+" -> "+self.chapter.getTranslation()))
    def initWidgets(self):
        self.main_frame = tk.CTkFrame(self.frame,width=400,height=400)
        self.title_label = tk.CTkLabel(self.frame, textvariable=(self.chapter_name), font=("Play",30,"bold"),bg_color="#1f538d")
        self.counting = tk.CTkLabel(self.main_frame,textvariable=self.count_var, font=("Play",15,"bold"))
        self.word_frame=tk.CTkFrame(self.main_frame)
        self.word = tk.CTkLabel(self.word_frame, textvariable=self.word_var, font=("Play",18,"bold"))
        self.button_frame = tk.CTkFrame(self.main_frame)
        self.previous_button = tk.CTkButton(self.button_frame, text="<",font=("Play",15,"bold"), width=25, height=25, command=self.previous_button_fun)
        self.next_button = tk.CTkButton(self.button_frame, text=">",font=("Play",15,"bold"), width=25, height=25, command=self.next_button_fun)
        self.previous_button.grid(row=0,column=0)
        self.next_button.grid(row=0,column=1)
        self.menu_button = tk.CTkButton(self.frame, text="Powrót", command=self.go_back)
    def initPacks(self):
        self.packFrame()
        self.title_label.pack(ipady=9, fill=tk.X, anchor=tk.N, expand=True)
        self.main_frame.pack(anchor=tk.CENTER, fill=tk.X, expand=True)
        self.counting.pack(anchor=tk.N, expand=True)
        self.word_frame.pack(ipadx=10,anchor=tk.CENTER, expand=True, padx=20, pady=(30,10))
        self.word.pack()
        self.button_frame.pack(anchor=tk.S, expand=True, pady=(0,10))
        self.menu_button.pack(anchor=tk.SE, expand=True)

    def previous_button_fun(self):
        self.chapter.previousWord()
        self.update()

    def next_button_fun(self):
        self.chapter.nextWord()
        self.update()

    def update(self):
        self.word_var.set(self.chapter.getWord()+" -> "+self.chapter.getTranslation())
        self.count_var.set(str(self.chapter.current_index + 1)+" / "+str(self.steps))

    def go_back(self):self.pushNewDelCur(ChapterMenuState(self.frame.master, self.state_manager_ptr))




class TeacherMenuState(State):
    def __init__(self, master: tk.CTk, state_manager:State_Manager) -> None:
        super().__init__(master, state_manager)
        self.packFrame()
        self.title_label = tk.CTkLabel(self.frame, text="Panel nauczyciela", font=("Play",30,"bold"),bg_color="#1f538d")
        self.title_label.pack(ipady=9, fill=tk.X, anchor=tk.N)
        self.emptyframe = tk.CTkFrame(self.frame)
        self.emptyframe.pack(fill=tk.X)
        TeacherMainFrame(self.emptyframe,self.go_to_chapterManager,self.go_to_studentStatistic, self.go_to_chapterStats, self.refresh)
        self.logout_button = tk.CTkButton(self.frame, text="Wyloguj", command=self.logout_fun)
        self.logout_button.pack(anchor=tk.S, expand=True,pady=(0,10))

    def logout_fun(self):
        global global_variables
        global_variables.id_user=0
        global_variables.isTeacher=False
        AutoLogin.del_current_data()
        self.pushNewDelCur(LoginState(self.frame.master, self.state_manager_ptr))   

    def go_to_chapterManager(self, class_data): self.pushNewDelCur(ChapterManager(self.frame.master, self.state_manager_ptr, class_data))
    def go_to_chapterStats(self, data_list:list): self.pushNewDelCur(ChapterStats(self.frame.master, self.state_manager_ptr, data_list))
    def go_to_studentStatistic(self, data_list:list): self.pushNewDelCur(StudentStatistic(self.frame.master, self.state_manager_ptr, data_list))

    def refresh(self):
        self.pushNewDelCur(TeacherMenuState(self.frame.master, self.state_manager_ptr))




class ChapterManager(State):
    def __init__(self, master: tk.CTk, state_manager:State_Manager, class_data) -> None:
        super().__init__(master, state_manager)
        self.packFrame()
        self.title_label = tk.CTkLabel(self.frame, text="Zarządzanie tematami", font=("Play",30,"bold"),bg_color="#1f538d")
        self.title_label.pack(ipady=9, fill=tk.X, anchor=tk.N)
        self.emptyframe = tk.CTkFrame(self.frame)
        self.emptyframe.pack(fill=tk.X)
        TeacherChapterManagerFrame(self.emptyframe,self.go_to_edit, class_data)
        self.menu_button = tk.CTkButton(self.frame, text="Powrót", command=self.go_back)
        self.menu_button.pack(anchor=tk.SE, expand=True)

    def go_back(self):self.pushNewDelCur(TeacherMenuState(self.frame.master, self.state_manager_ptr))
    def go_to_edit(self, topic_id, topic_name, class_data): self.pushNewDelCur(EditorState(self.frame.master, self.state_manager_ptr, topic_id, topic_name, class_data))
    



class ChapterStats(State):
    def __init__(self, master: tk.CTk, state_manager:State_Manager, data_list:list) -> None:
        super().__init__(master, state_manager)
        self.packFrame()
        self.data_list = data_list
        self.title_label = tk.CTkLabel(self.frame, text=self.data_list[0][0], font=("Play",30,"bold"),bg_color="#1f538d")
        self.title_label.pack(ipady=9, fill=tk.X, anchor=tk.N)
        try:
            if self.data_list[0][1]:
                TeacherChapterStatsFrame(self.frame, data_list)
        except:
            self.mainframe = tk.CTkFrame(self.frame, bg_color="#292929")
            self.emptyLabel = tk.CTkLabel(self.mainframe, text="Brak danych", height=330, font=("Play", 20))
            self.mainframe.pack(fill=tk.X)
            self.emptyLabel.pack(anchor=tk.CENTER, expand=True)
        self.menu_button = tk.CTkButton(self.frame, text="Powrót", command=self.go_back)
        self.menu_button.pack(anchor=tk.SE, expand=True)

    def go_back(self):self.pushNewDelCur(TeacherMenuState(self.frame.master, self.state_manager_ptr))




class StudentStatistic(State):
    def __init__(self, master: tk.CTk, state_manager:State_Manager, data_list:list) -> None:
        super().__init__(master, state_manager)
        self.packFrame()
        self.title_label = tk.CTkLabel(self.frame, text=data_list[0][0], font=("Play",30,"bold"),bg_color="#1f538d")
        self.title_label.pack(ipady=9, fill=tk.X, anchor=tk.N)
        try:
            if data_list[0][1]:
                TeacherStudentStatisticFrame(self.frame, data_list)
        except:
            self.mainframe = tk.CTkFrame(self.frame, bg_color="#292929")
            self.emptyLabel = tk.CTkLabel(self.mainframe, text="Brak danych", height=330, font=("Play", 20))
            self.mainframe.pack(fill=tk.X)
            self.emptyLabel.pack(anchor=tk.CENTER, expand=True)
        self.menu_button = tk.CTkButton(self.frame, text="Powrót", command=self.go_back)
        self.menu_button.pack(anchor=tk.SE, expand=True)

    def go_back(self):self.pushNewDelCur(TeacherMenuState(self.frame.master, self.state_manager_ptr))




class RegisterState(State):
    def __init__(self, master: tk.CTk, state_manager:State_Manager) -> None:
        super().__init__(master, state_manager)
        self.initVariables()
        self.initWidgets()
        self.initPacks()

    def initVariables(self):
        self.annoucment_var = tk.StringVar()
        self.checkbox_var = tk.IntVar()
        self.ph = PasswordHasher()
    def initWidgets(self):
        self.title_label = tk.CTkLabel(self.frame, text="Rejestracja", font=("Play",30,"bold"),bg_color="#1f538d")
        self.main_frame = tk.CTkFrame(self.frame)
        self.empty_frame = tk.CTkFrame(self.main_frame)
        self.menu_button = tk.CTkButton(self.frame, text="Powrót", command=self.go_back)
    def initPacks(self):
        self.packFrame()
        self.title_label.pack(ipady=9, fill=tk.X, anchor=tk.N)
        self.main_frame.pack(expand=True,anchor=tk.CENTER,ipady=5)
        self.empty_frame.grid(row=0,column=0)
        self.content()
        self.login_frame.pack(anchor=tk.S)
        self.annoucment = tk.CTkLabel(self.main_frame, textvariable=self.annoucment_var).grid(row=1,column=0)
        self.login_button = tk.CTkButton(self.main_frame, text="Zarejestruj", command=self.regiser).grid(row=2,column=0)
        self.menu_button.pack(anchor=tk.SE,expand=True)
    def content(self):
        self.login_frame = tk.CTkFrame(self.empty_frame)
        
        self.login_label = tk.CTkLabel(self.login_frame, text="Login").grid(row=0,column=0,ipadx=10)
        self.login_entry = tk.CTkEntry(self.login_frame)
        self.login_entry.grid(row=0,column=1,pady=(5,0))

        self.pass_label = tk.CTkLabel(self.login_frame, text="Hasło").grid(row=1,column=0,ipadx=10)
        self.pass_entry = tk.CTkEntry(self.login_frame,show='*')
        self.pass_entry.grid(row=1,column=1,pady=(5,0))

        self.pass2_label = tk.CTkLabel(self.login_frame, text="Powtórz").grid(row=2,column=0,ipadx=10)
        self.pass2_entry = tk.CTkEntry(self.login_frame,show='*')
        self.pass2_entry.grid(row=2,column=1,pady=(5,0))

        self.checkbox = tk.CTkCheckBox(self.login_frame,text="Konto nauczyciela", variable=self.checkbox_var)
        self.checkbox.grid(row=3,column=1,pady=(5,2))

        self.login_entry.bind("<Return>", self.focus_next)
        self.pass_entry.bind("<Return>", self.focus_next1)
        self.pass2_entry.bind("<Return>", self.regiser)
        
    def focus_next(self,event=""):
        self.pass_entry.focus()
    def focus_next1(self,event=""):
        self.pass2_entry.focus()

    def regiser(self,event=""):
        login = self.login_entry.get()
        if len(login)!=0:
            if len(self.pass_entry.get())!=0:
                if len(self.pass2_entry.get())!=0:
                    if len(login)>=4:
                        if len(login)<=30:
                            if len(self.pass_entry.get())>=4:
                                self.checkLoginStudent(login)
                            else:
                                self.annoucment_var.set("Hasło zbyt krótkie (min. 4 znaki)")
                        else:
                            self.annoucment_var.set("Login zbyt długi (max. 30 znaków)")  
                    else:
                        self.annoucment_var.set("Login zbyt krótki (min. 4 znaki)")
                else:
                    self.annoucment_var.set("Nie powtórzono hasła")
            else:
                self.annoucment_var.set("Nie podano hasła")
        else:
            self.annoucment_var.set("Nie podano loginu")

    def checkLoginStudent(self,login):
        query = f"SELECT * FROM uczniowie WHERE login = '{login}'"
        global_variables.mycursor.execute(query)
        result = global_variables.mycursor.fetchall()
        i,exist=0,False
        while i<len(result):
            if login==result[i][1]:
                exist=True
                break
            i+=1
        if exist:
            self.annoucment_var.set("Taki login już istnieje")
        else:
            self.checkLoginTeacher(login)

    def checkLoginTeacher(self,login):
        query = f"SELECT * FROM nauczyciele WHERE login = '{login}'"
        global_variables.mycursor.execute(query)
        result = global_variables.mycursor.fetchall()
        i,exist=0,False
        while i<len(result):
            if login==result[i][1]:
                exist=True
                break
            i+=1
        if exist:
            self.annoucment_var.set("Taki login już istnieje")
        else:
            self.insertIntoDatabase(login)

    def insertIntoDatabase(self,login):
        if self.pass_entry.get() != self.pass2_entry.get():
                self.annoucment_var.set("Podano różne hasła")
        elif self.checkbox_var.get() == 1:
            query = f"INSERT INTO `nauczyciele`(`login`, `haslo`) VALUES ('{login}','{self.ph.hash(self.pass_entry.get())}')"
            global_variables.mycursor.execute(query)
            global_variables.mydb.commit()
            self.checkTeacher(login)
        elif self.checkbox_var.get() == 0:
            query = f"INSERT INTO `uczniowie`(`login`, `haslo`) VALUES ('{login}','{self.ph.hash(self.pass_entry.get())}')"
            global_variables.mycursor.execute(query)
            global_variables.mydb.commit()
            self.checkStudent(login)

    def checkStudent(self,login):
        global global_variables
        query = f"SELECT * FROM uczniowie WHERE login = '{login}'"
        global_variables.mycursor.execute(query)
        result = global_variables.mycursor.fetchall()
        i=0
        while i<len(result):
            if login==result[i][1]:
                index=i
                break
            i+=1
        global_variables.id_user = result[index][0]
        global_variables.id_class = result[index][3]
        self.pushNewDelCur(ChapterMenuState(self.frame.master, self.state_manager_ptr))
        
    def checkTeacher(self,login):
        global global_variables
        query = f"SELECT * FROM nauczyciele WHERE login = '{login}'"
        global_variables.mycursor.execute(query)
        result = global_variables.mycursor.fetchall()
        i=0
        while i<len(result):
            if login==result[i][1]:
                index=i
                break
            i+=1
        global_variables.id_user = result[index][0]
        global_variables.isTeacher = True
        self.pushNewDelCur(TeacherMenuState(self.frame.master, self.state_manager_ptr))
            
    def go_back(self):self.pushNewDelCur(LoginState(self.frame.master, self.state_manager_ptr))





class LoginState(State):
    def __init__(self, master: tk.CTk, state_manager:State_Manager) -> None:
        super().__init__(master, state_manager)
        self.ph = PasswordHasher()
        self.initVariables()
        self.initWidgets()
        self.initPacks()
        

    def initVariables(self):
        self.annoucment_var = tk.StringVar()
        self.auto_login = AutoLogin()
    def initWidgets(self):
        self.title_label = tk.CTkLabel(self.frame, text="Logowanie", font=("Play",30,"bold"),bg_color="#1f538d")
        self.main_frame = tk.CTkFrame(self.frame)
        self.empty_frame = tk.CTkFrame(self.main_frame)
        self.empty_label = tk.CTkLabel(self.frame, text="")
    def initPacks(self):
        self.packFrame()
        self.title_label.pack(ipady=9, fill=tk.X, anchor=tk.N)
        self.main_frame.pack(expand=True,anchor=tk.CENTER,ipady=5)
        self.empty_frame.grid(row=0,column=0)
        self.content()
        self.login_frame.pack(anchor=tk.S)
        self.annoucment = tk.CTkLabel(self.main_frame, textvariable=self.annoucment_var).grid(row=1,column=0)
        self.login_button = tk.CTkButton(self.main_frame, text="Zaloguj", command=self.login).grid(row=2,column=0)
        self.register_button = tk.CTkButton(self.main_frame, text="Rejestracja", command=self.go_to_register).grid(row=3,column=0,pady=5)
        self.empty_label.pack(anchor=tk.SE,expand=True)
    def content(self):
        self.login_frame = tk.CTkFrame(self.empty_frame)
        
        self.login_label = tk.CTkLabel(self.login_frame, text="Login").grid(row=0,column=0,ipadx=10)
        self.login_entry = tk.CTkEntry(self.login_frame)
        self.login_entry.grid(row=0,column=1,pady=(5,0))

        self.pass_label = tk.CTkLabel(self.login_frame, text="Hasło").grid(row=1,column=0,ipadx=10)
        self.pass_entry = tk.CTkEntry(self.login_frame,show='*')
        self.pass_entry.grid(row=1,column=1,pady=(5,0))

        self.checkbox = tk.CTkCheckBox(self.login_frame,text="Zapamiętaj")
        self.checkbox.grid(row=2,column=1,pady=(5,2))

        self.login_entry.bind("<Return>", self.focus_next)
        self.pass_entry.bind("<Return>", self.login)
    
    def go_to_register(self):
        self.pushNewDelCur(RegisterState(self.frame.master, self.state_manager_ptr))

    def focus_next(self,event=""):
        self.pass_entry.focus()

    def login(self,event=""):
        login = self.login_entry.get()
        passwd = self.pass_entry.get()
        if len(login)>0:
            if len(passwd)>0:
                self.checkStudent(login,passwd)
            else:
                self.annoucment_var.set("Nie podano hasła")
        else:
            self.annoucment_var.set("Nie podano loginu")

    def checkStudent(self,login,passwd):
        global global_variables
        query = f"SELECT * FROM uczniowie WHERE login = '{login}'"
        global_variables.mycursor.execute(query)
        result = global_variables.mycursor.fetchall()
        i,exist=0,False
        while i<len(result):
            if login==result[i][1]:
                exist=True
                index=i
                break
            i+=1
        if exist:
            try:
                if self.ph.verify(result[index][2], passwd):
                    global_variables.id_user = result[index][0]
                    global_variables.id_class = result[index][3]
                    if self.checkbox.get():
                        self.auto_login.set_new_data(login, passwd)
                    self.pushNewDelCur(ChapterMenuState(self.frame.master, self.state_manager_ptr))
            except:
                self.annoucment_var.set("Błędne hasło")
                self.pass_entry.delete(0, tk.END)
        else:
            self.checkTeacher(login,passwd)
        
    def checkTeacher(self,login,passwd):
        global global_variables
        query = f"SELECT * FROM nauczyciele WHERE login = '{login}'"
        global_variables.mycursor.execute(query)
        result = global_variables.mycursor.fetchall()
        i,exist=0,False
        while i<len(result):
            if login==result[i][1]:
                exist=True
                index=i
                break
            i+=1
        if exist:
            try:
                if self.ph.verify(result[index][2], passwd):
                    global_variables.id_user = result[index][0]
                    global_variables.isTeacher = True
                    if self.checkbox.get():
                        self.auto_login.set_new_data(login, passwd)
                    self.pushNewDelCur(TeacherMenuState(self.frame.master, self.state_manager_ptr))
            except:
                self.annoucment_var.set("Błędne hasło")
                self.pass_entry.delete(0, tk.END)
        else:
            self.annoucment_var.set("Taki login nie istnieje")




class App:
    def __init__(self) -> None:

        self.window = tk.CTk()
        self.window.geometry("610x500")
        self.window.minsize(610,500)
        self.window.maxsize(610,500)
        self.window.title("Teachme")
        try:
            try:
                self.window.wm_iconbitmap("./zowIcon.ico")
            except:
                self.window.wm_iconbitmap("../zowIcon.ico")
        except:
            pass
        self.state_manager = State_Manager()
        self.auto_login = AutoLogin()
        self.ph = PasswordHasher()

        while not global_variables.is_connected:
            if messagebox.askretrycancel("Błąd połączenia z bazą","Chcesz spróbować jeszcze raz?"):
                if tryAgain():
                    break
            else:
                raise Exception
            
        if self.auto_login.is_exist():
            self.check_auto_login()
        else:
            self.state_manager.push_state(LoginState(self.window, self.state_manager))

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def on_closing(self):
        if messagebox.askyesno("Wychodzisz?", "Jesteś pewien?"):
            self.window.destroy()

    def __del__(self):
        try:
            global_variables.mydb.close()
        except:
            pass

    def _auto_login_(self, login:str, password:str):
        global global_variables
        query = f"SELECT * FROM uczniowie WHERE login = '{login}'"
        global_variables.mycursor.execute(query)
        result = global_variables.mycursor.fetchall()
        i,exist=0,False
        while i<len(result):
            if login==result[i][1]:
                exist=True
                index=i
                break
            i+=1
        if exist:
            try:
                if self.ph.verify(result[index][2], password):
                    global_variables.id_user= result[index][0]
                    global_variables.id_class = result[index][3]
                    global_variables.isTeacher = False
                    self.state_manager.push_state(ChapterMenuState(self.window, self.state_manager))
            except:
                pass
        else:
            query = f"SELECT * FROM nauczyciele WHERE login = '{login}'"
            global_variables.mycursor.execute(query)
            result = global_variables.mycursor.fetchall()
            i,exist=0,False
            while i<len(result):
                if login==result[i][1]:
                    exist=True
                    index=i
                    break
                i+=1
            if exist:
                try:
                    if self.ph.verify(result[index][2], password):
                        global_variables.id_user = result[index][0]
                        global_variables.isTeacher = True                               
                        self.state_manager.push_state(TeacherMenuState(self.window, self.state_manager))
                except:
                    pass
            else:
                pass

    def check_auto_login(self):
            login_data = self.auto_login.get_login_data()
            self._auto_login_(login_data[0], login_data[1])

tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")
try:
    App()
except Exception:...