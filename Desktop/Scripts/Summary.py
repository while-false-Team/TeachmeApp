import customtkinter as tk
from WordsModule import Words


class SummaryTable:
    def __init__(self, master:tk.CTkFrame, words:Words) -> None:
        
        self.frameGrid = tk.CTkScrollableFrame(master=master, width=450, height=300)
        self.frameGrid.columnconfigure(0)
        self.frameGrid.columnconfigure(1)
        self.frameGrid.columnconfigure(2)
        self.frameGrid.columnconfigure(3)
        
        tk.CTkLabel(self.frameGrid, text="Słówko", bg_color="#1f538d", font=("Play",16,"bold")).grid(row=0, column=0, ipadx = 10, ipady = 10, sticky=tk.W+tk.E)
        tk.CTkLabel(self.frameGrid, text="Tłumaczenie", bg_color="#1f538d", font=("Play",16,"bold")).grid(row=0, column=1, ipadx = 10, ipady = 10, sticky=tk.W+tk.E)
        tk.CTkLabel(self.frameGrid, text="Ile błędów", bg_color="#1f538d", font=("Play",16,"bold")).grid(row=0, column=2, ipadx = 10, ipady = 10, sticky=tk.W+tk.E)
        tk.CTkLabel(self.frameGrid, text="Błędy", bg_color="#1f538d", font=("Play",16,"bold")).grid(row=0, column=3, ipadx = 10, ipady = 10, sticky=tk.W+tk.E)
        i = 1

        words.finishedWords = self.sortTableByMistakes(words.finishedWords)
        self.finishedWords = words.finishedWords
        for word in words.finishedWords:
            tk.CTkLabel(self.frameGrid, text=word.word).grid(row=i, column=0, sticky=tk.W+tk.E, ipadx = 10, ipady = 10)
            tk.CTkLabel(self.frameGrid, text=word.translation).grid(row=i, column=1, sticky=tk.W+tk.E, ipadx = 10, ipady = 10)
            tk.CTkLabel(self.frameGrid, text=str(word.mistakes)).grid(row=i, column=2, sticky=tk.W+tk.E, ipadx = 10, ipady = 10)
            fun = lambda index=i-1: self.konstruktButton(index)
            tk.CTkButton(self.frameGrid, text="Pokaż błędy", command=fun).grid(row=i, column=3, sticky=tk.W+tk.E)
            i+=1
            
        self.frameGrid.pack(expand=True, anchor=tk.CENTER)

        self.inLabel= tk.StringVar(value="")
        self.mistakesGrid = tk.CTkScrollableFrame(master=master, orientation="horizontal", width=450, height=40)
        tk.CTkLabel(self.mistakesGrid, textvariable=self.inLabel, font=("Play",13,"italic")).grid(row=0,column=0)
        self.mistakesGrid.pack(expand=True, anchor=tk.CENTER,pady=10)


    def sortTableByMistakes(self, tab:list):
        index,n,minimalna=0,0,0
        while 1:
            tab2=[]
            if n == len(tab):
                return tab
            for i in range(n,len(tab)):
                tab2.append(tab[i].mistakes)
            minimalna=tab2[0]
            for i in (tab2):
                if i>minimalna:
                    minimalna=i
            index=n+tab2.index(minimalna)
            if tab[n]!=tab[index]:
                tab[n],tab[index]=tab[index],tab[n]
            n+=1         

    def konstruktButton(self, index):
        mistakes = str()
        for mistake in self.finishedWords[index].mistakes_words:
            mistakes += (mistake + ", ")
        if mistakes == "":
            text="Brak błędów"
        else:
            text=mistakes[0:-2]
        self.inLabel.set(self.finishedWords[index].word+": "+text)   
