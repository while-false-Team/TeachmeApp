import customtkinter as tk
from tkinter import messagebox
from TopicDataModule import *
import pyperclip as pc
from ClassDataModule import *
import global_variables
from random import randint as rand

class TeacherMainFrame:
    class TabOne:
        def __init__(self, master:tk.CTkFrame, class_data:ClassDataManager.ClassData, go_to_chapterManager, go_to_chapterStatistic) -> None:
            self.frame = master
            self.class_data = class_data
            self.go_to_chapterManager=go_to_chapterManager
            self.go_to_chapterStiatistic = go_to_chapterStatistic
            self.chapterScrollBar = tk.CTkScrollableFrame(self.frame, width=150, bg_color="#292929")
            self.chapterScrollBar.pack(anchor=tk.N,pady=(0,5))
            
            iterator=0
            for topic in self.class_data.get_topics():
                fun = lambda topic_id=topic[0]:self.konstruct_topic_button(topic_id)
                self.Button = tk.CTkButton(self.chapterScrollBar, text=topic[1], command=fun)
                self.Button.pack(pady=(0,2))
                iterator+=1
            if iterator==0:
                self.EmptyLabel = tk.CTkLabel(self.chapterScrollBar, text="Brak tematów", font=("Play", 16))
                self.EmptyLabel.pack()
            self.newButtonFrame = tk.CTkFrame(self.frame, height=30)
            fun = lambda : self.go_to_chapterManager(self.class_data)
            self.newButton = tk.CTkButton(self.newButtonFrame, text="Zarządzaj",font=("Play",15), command=fun)
            self.newButtonFrame.pack(anchor=tk.S)
            self.newButton.pack()

        def konstruct_topic_button(self, topic_id):
            self.go_to_chapterStiatistic(self.class_data.getStudentsDataForTopic(topic_id))


    class TabTwo:
        def __init__(self, master:tk.CTkFrame, class_data:ClassDataManager.ClassData, go_to_studentStatistic, refresh) -> None:
            self.frame = master
            self.class_data = class_data
            self.go_to_studentStatistic=go_to_studentStatistic
            self.refresh = refresh
            self.chapterScrollBar = tk.CTkScrollableFrame(self.frame, width=315, bg_color="#292929")
            self.chapterScrollBar.pack()
            
            iterator=0
            for student in self.class_data.getAllStudentsForClass():
                fun = lambda id=student[0]: self.konstruct_student_button(id)
                tk.CTkButton(self.chapterScrollBar, text=student[1],width=270, command=fun).grid(row=iterator, column=0, pady=(0,2))
                fun = lambda id=student[0], name=student[1]: self.konstruct_delete_student_button(id,name)
                tk.CTkButton(self.chapterScrollBar, text="X",width=30, command=fun, fg_color="#B30000", font=("Play",16,"bold")).grid(row=iterator, column=1, pady=(0,2),padx=(2,0))
                iterator+=1
            if iterator==0:
                self.EmptyLabel = tk.CTkLabel(self.chapterScrollBar, text="Brak uczniów", font=("Play", 16))
                self.EmptyLabel.pack()
    
        def konstruct_student_button(self, student_id):
            self.go_to_studentStatistic(self.class_data.getAllStudentsData(student_id))

        def konstruct_delete_student_button(self, student_id, student_name):
            if messagebox.askyesno("Usuwanie ucznia", f"Czy napewno chcesz usunąć ucznia {student_name}\nz klasy?"):
                query = f"UPDATE uczniowie SET id_klasy=NULL WHERE id_ucznia={student_id};"
                global_variables.mycursor.execute(query)
                global_variables.mydb.commit()
                self.refresh()


    class TabThree:
        def __init__(self, master:tk.CTkFrame, class_data:ClassDataManager.ClassData) -> None:
            self.frame = master
            self.class_data = class_data
            self.code = self.class_data.class_code
            self.className = tk.CTkLabel(self.frame,text=self.code,font=("Play",40))
            self.className.pack(expand=True,anchor=tk.CENTER)
            self.copyButton = tk.CTkButton(self.frame, text="Skopiuj",font=("Play",13),width=40,height=20, command=self.copyCode)
            self.copyButton.pack(pady=(0,5))

        def copyCode(self):pc.copy(self.code)

    class RightFrame:
        def __init__(self, master:tk.CTkFrame, class_data:ClassDataManager.ClassData,go_to_chapterManager, go_to_studentStatistic, go_to_chapterStatistic, refresh) -> None:
            self.class_data = class_data
            self.className = tk.CTkLabel(master,text=self.class_data.class_name,font=("Play",17,"bold"))
            self.className.grid(row=0,column=1,sticky=tk.N,pady=(5,0))
            self.tabs = tk.CTkTabview(master,width=440,height=300,bg_color="#292929")
            self.tabs.add("Tematy klasy")
            self.tabs.add("Uczniowie")
            self.tabs.add("Kod klasy")
            TeacherMainFrame.TabOne(self.tabs.tab("Tematy klasy"),self.class_data,go_to_chapterManager, go_to_chapterStatistic)
            TeacherMainFrame.TabTwo(self.tabs.tab("Uczniowie"),self.class_data, go_to_studentStatistic, refresh)
            TeacherMainFrame.TabThree(self.tabs.tab("Kod klasy"), self.class_data)
            self.tabs.grid(row=0,column=1,sticky=tk.S)

        def destroy(self):
            self.className.destroy()
            self.tabs.destroy()
        
    def __init__(self, master:tk.CTkFrame,go_to_chapterManager, go_to_studentStatistic, go_to_chapterStatistic, refresh) -> None:
        self.frame=master
        self.go_to_chapterManager=go_to_chapterManager
        self.go_to_studentStatistic=go_to_studentStatistic
        self.go_to_chapterStatistic=go_to_chapterStatistic
        self.refresh = refresh
        self.class_data_manager = ClassDataManager(global_variables.id_user)
        self.current_class_index=0
        if len(self.class_data_manager.classDataList)>0:
            self.mainframe = tk.CTkFrame(self.frame)
            self.classScrollBar = tk.CTkScrollableFrame(self.mainframe, width=150, height=300, bg_color="#292929")
            self.mainframe.pack(fill=tk.X)

            self.newButtonFrame = tk.CTkFrame(self.mainframe, height=30, bg_color="#292929")
            self.newButton = tk.CTkButton(self.newButtonFrame, text="Nowa klasa", anchor="center",width=75, command=self.newClass)
            self.delButton = tk.CTkButton(self.newButtonFrame, text="Usuń klasę", anchor="center",width=75, command=self.delClass)

            iterator=0
            for classes in self.class_data_manager.classDataList:
                fun = lambda index=iterator:self.konstruct_class_button(index)
                tk.CTkButton(self.classScrollBar, text=classes.class_name, anchor="center", command=fun, font=("Play", 20)).pack(pady=(2,0))
                iterator+=1

            self.class_name_entry = tk.CTkEntry(self.classScrollBar,width=140,font=("Play", 16))
            self.class_name_entry.pack(expand=True,anchor=tk.CENTER,pady=10)
            self.class_name_entry.bind('<Return>',self.newClass)
            self.right_frame = self.RightFrame(self.mainframe, self.class_data_manager.classDataList[0],self.go_to_chapterManager, self.go_to_studentStatistic, self.go_to_chapterStatistic, self.refresh)
            self.classScrollBar.grid(row=0, column=0, sticky=tk.N,pady=(0,25))
            self.newButton.grid(row=0,column=0,padx=(6,0))
            self.delButton.grid(row=0,column=1)
            self.newButtonFrame.grid(row=0, column=0,sticky=tk.S,ipadx=4)

            self.emptyframe = tk.CTkFrame(self.frame, bg_color="#292929")
            self.emptyframe.pack(fill=tk.X,pady=(5,0))
            self.annoucement_var = tk.StringVar(value="")
            self.annoucement = tk.CTkLabel(self.emptyframe, textvariable=self.annoucement_var)
            self.annoucement.pack(anchor=tk.CENTER)

        else:
            self.emptyLabel = tk.CTkLabel(self.frame, text="Nie masz jeszcze żadnych klas.\n\nPodaj nazwę dla klasy:", font=("Play", 16))
            self.emptyLabel.pack(fill=tk.X,expand=True,anchor=tk.N,pady=(100,0))
            self.class_name_entry = tk.CTkEntry(self.frame,width=140)
            self.class_name_entry.pack(expand=True,anchor=tk.CENTER,pady=10)
            self.class_name_entry.bind('<Return>',self.newClass)
            self.firstButton = tk.CTkButton(self.frame, text="Dodaj pierwszą klasę", anchor="center", command=self.newClass)
            self.firstButton.pack(expand=True,anchor=tk.S,pady=(0,120))
            self.emptyframe = tk.CTkFrame(self.frame, bg_color="#292929")
            self.emptyframe.pack(fill=tk.X,pady=(5,0))
            self.annoucement_var = tk.StringVar(value="")
            self.annoucement = tk.CTkLabel(self.emptyframe, textvariable=self.annoucement_var)
            self.annoucement.pack(anchor=tk.CENTER)

    def delClass(self):
        if messagebox.askyesno("Czy jesteś pewien?", f"Czy jesteś pewien że chcesz usunąć klasę {self.class_data_manager.classDataList[self.current_class_index].class_name}\nZmiany będą nie odwracalne!"):
            query_del_words = f"DELETE FROM slowka WHERE slowka.id_tematu IN (SELECT id_tematu FROM tematy WHERE id_klasy={self.class_data_manager.classDataList[self.current_class_index].class_id});"
            query_del_topic_data = f"DELETE FROM `dane_tematow` WHERE id_tematu IN (SELECT id_tematu FROM tematy WHERE id_klasy={self.class_data_manager.classDataList[self.current_class_index].class_id})"
            query_del_topics = f"DELETE FROM tematy WHERE id_klasy={self.class_data_manager.classDataList[self.current_class_index].class_id};"
            query_del_class = f"DELETE FROM klasy WHERE id_klasy={self.class_data_manager.classDataList[self.current_class_index].class_id};"

            global_variables.mycursor.execute(query_del_words)
            global_variables.mycursor.execute(query_del_topic_data)
            global_variables.mycursor.execute(query_del_topics)
            global_variables.mycursor.execute(query_del_class)
            global_variables.mydb.commit()
            self.refresh()



    def newClass(self, event=""):
        self.entry=self.class_name_entry.get()
        if self.entry!='' and self.entry[0]!=' ':
            if len(self.entry)<=10:
                query = "SELECT `kod_klasy` FROM `klasy`"
                global_variables.mycursor.execute(query)
                self.usedCodes=global_variables.mycursor.fetchall()
                self.repeat=True
                while self.repeat:
                    self.repeat=False
                    self.code=hex(rand(1048576,16777215)).upper()[2:]
                    for n in self.usedCodes:
                        if n[0] == self.code: 
                            self.repeat=True
                            break
                query = f"INSERT INTO klasy(nazwa_klasy, id_nauczyciela, kod_klasy) VALUES ('{self.class_name_entry.get()}',{global_variables.id_user},'{self.code}')"
                global_variables.mycursor.execute(query)
                global_variables.mydb.commit()
                self.refresh()
            else:self.annoucement_var.set("Nazwa klasy za długa (max. 10 znaków)")
        else:self.annoucement_var.set("Nie podano nazwy klasy")

    def konstruct_class_button(self, class_index):
        self.current_class_index = class_index
        self.right_frame.destroy()
        self.right_frame = self.RightFrame(self.mainframe, self.class_data_manager.classDataList[class_index],self.go_to_chapterManager,self.go_to_studentStatistic,self.go_to_chapterStatistic, self.refresh)

class TeacherChapterManagerFrame:

    def __init__(self, master:tk.CTkFrame,go_to_edit, class_data:ClassDataManager.ClassData=None) -> None:
        self.frame=master
        self.go_to_edit=go_to_edit
        self.class_data = class_data
        self.topics = self.class_data.get_topics()
        if len(self.topics)>0:
            self.mainframe = tk.CTkFrame(self.frame)
            self.classScrollBar = tk.CTkScrollableFrame(self.mainframe, height=330, bg_color="#292929")
            self.mainframe.pack(fill=tk.X)
            for topic in self.topics:
                fun = lambda id=topic[0], name=topic[1]: self.go_to_edit(id, name, self.class_data)
                tk.CTkButton(self.classScrollBar, text=topic[1], anchor="center",font=("Play", 16), width=200, command=fun).pack(pady=(5,0))
            self.classScrollBar.pack(fill=tk.X)
            self.ButtonFrame = tk.CTkFrame(self.frame, height=30, bg_color="#292929")
            self.newButton = tk.CTkButton(self.ButtonFrame, text="Stwórz nowy temat", anchor="center", command=self.newChapter)
            self.ButtonFrame.pack()
            self.newButton.pack()
        else:
            self.emptyLabel = tk.CTkLabel(self.frame, text="Brak tematów", font=("Play", 20),height=183)
            self.emptyLabel.pack(fill=tk.X,expand=True,anchor=tk.CENTER)
            self.firstButton = tk.CTkButton(self.frame, text="Dodaj pierwszy temat", anchor="center", command=self.newChapter)
            self.firstButton.pack(expand=True,anchor=tk.CENTER,pady=(0,120))
    
    def konstruct_topic_button(self, topic_id, topic_name):
        self.go_to_edit(topic_id, topic_name)

    def newChapter(self):
        query = f"INSERT INTO `tematy`(`nazwa_tematu`,`id_klasy`) VALUES ('Nowy temat', {self.class_data.class_id});"
        global_variables.mycursor.execute(query)
        global_variables.mydb.commit()
        topic_id = self.class_data.get_topics()[-1][0]
        self.go_to_edit(topic_id, "Nowy temat", self.class_data)
        query = f"SELECT id_ucznia FROM uczniowie WHERE id_klasy={self.class_data.class_id}"
        global_variables.mycursor.execute(query)
        result = global_variables.mycursor.fetchall()
        for id in result:
            insert = f"INSERT INTO `dane_tematow`(`id_tematu`, `id_ucznia`, `ile_ukonczen`, `data_ostatniego_uruchomienia`) VALUES ({topic_id},{id[0]},0,'0000-00-00')"
            global_variables.mycursor.execute(insert)
        global_variables.mydb.commit()



class TeacherChapterStatsFrame:
    def __init__(self, master:tk.CTkFrame, data_list:list) -> None:
        self.frame=master
        self.data_list = data_list
        self.classScrollBar = tk.CTkScrollableFrame(self.frame, height=330, bg_color="#292929")
        self.classScrollBar.pack(fill=tk.X,expand=True)
        tk.CTkLabel(self.classScrollBar, text="Nazwa ucznia", font=("Play", 17),bg_color="#1f538d").grid(row=0,column=0,ipadx=40,pady=10)
        tk.CTkLabel(self.classScrollBar, text="Przyswojenie", font=("Play", 17),bg_color="#1f538d").grid(row=0,column=1,ipadx=30)
        tk.CTkLabel(self.classScrollBar, text="Ile ukończeń", font=("Play", 17),bg_color="#1f538d").grid(row=0,column=2,ipadx=0)
        tk.CTkLabel(self.classScrollBar, text="Ukończono", font=("Play", 17),bg_color="#1f538d").grid(row=0,column=3,ipadx=25)
        iterator=1
        for students in self.data_list:
            tk.CTkLabel(self.classScrollBar, text=students[1], font=("Play", 15)).grid(row=iterator,column=0)
            tk.CTkLabel(self.classScrollBar, text=students[4], font=("Play", 15)).grid(row=iterator,column=1)
            tk.CTkLabel(self.classScrollBar, text=students[2], font=("Play", 15)).grid(row=iterator,column=2)
            tk.CTkLabel(self.classScrollBar, text=students[3], font=("Play", 15)).grid(row=iterator,column=3)
            iterator+=1
            



class TeacherStudentStatisticFrame:
    def __init__(self, master:tk.CTkFrame, data_list:list) -> None:
        self.frame=master
        self.data_list = data_list
        self.classScrollBar = tk.CTkScrollableFrame(self.frame, height=330, bg_color="#292929")
        self.classScrollBar.pack(fill=tk.X,expand=True)
        tk.CTkLabel(self.classScrollBar, text="Nazwa tematu", font=("Play", 17),bg_color="#1f538d").grid(row=0,column=0,ipadx=40,pady=10)
        tk.CTkLabel(self.classScrollBar, text="Przyswojenie", font=("Play", 17),bg_color="#1f538d").grid(row=0,column=1,ipadx=30)
        tk.CTkLabel(self.classScrollBar, text="Ile ukończeń", font=("Play", 17),bg_color="#1f538d").grid(row=0,column=2,ipadx=0)
        tk.CTkLabel(self.classScrollBar, text="Ukończono", font=("Play", 17),bg_color="#1f538d").grid(row=0,column=3,ipadx=25)
        iterator=1
        for stats in self.data_list:
            tk.CTkLabel(self.classScrollBar, text=stats[1], font=("Play", 15)).grid(row=iterator,column=0)
            tk.CTkLabel(self.classScrollBar, text=stats[4], font=("Play", 15)).grid(row=iterator,column=1)
            tk.CTkLabel(self.classScrollBar, text=stats[2], font=("Play", 15)).grid(row=iterator,column=2)
            tk.CTkLabel(self.classScrollBar, text=stats[3], font=("Play", 15)).grid(row=iterator,column=3)
            iterator+=1