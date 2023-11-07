from random import randint as rand
from dbconnection import *

class Words:

    class Word:
        def __init__(self, word:str, translation:str) -> None:
            self.word = word
            self.translation = translation
            self.points = 0
            self.mistakes = 0
            self.mistakes_words = list()

    def __init__(self, chapter_id:int) -> bool:
        self.chapter_id = chapter_id
        self.neededPoints = 3
        self.initVariables()

    def initVariables(self):
        self.wordsList = list()
        query = f"SELECT nazwa_tematu FROM tematy WHERE id_tematu={self.chapter_id}"
        global_variables.mycursor.execute(query)
        self.chapter_name = global_variables.mycursor.fetchall()[0][0]

        query = f"SELECT slowko, tlumaczenie FROM slowka WHERE id_tematu= {self.chapter_id}"
        global_variables.mycursor.execute(query)

        table = global_variables.mycursor.fetchall()

        for word in table:
            self.wordsList.append(self.Word(word[0], word[1]))

        self.current_index = rand(0, len(self.wordsList)-1)
        self.finishedWords = []
        self.is_end = False
        
    def getWord(self):
        try:return self.wordsList[self.current_index].word
        except IndexError:self.is_end=True
    def getTranslation(self):
        try:return self.wordsList[self.current_index].translation
        except IndexError:self.is_end=True

    def checkCorrectness(self, translation:str, addPoints=True) -> bool:
        try:
            if self.wordsList[self.current_index].translation.lower() == translation.lower():
                if addPoints:self.incrementPoints()
                if self.wordsList[self.current_index].points>=self.neededPoints:
                    self.finishedWords.append(self.wordsList[self.current_index])
                    self.wordsList.pop(self.current_index)
                    if len(self.wordsList) == 0:
                        self.is_end = True
                    else: self.drawNewWord()
                else:self.drawNewWord()
                return True
            else:
                self.wordsList[self.current_index].mistakes_words.append(translation)
                self.wordsList[self.current_index].mistakes+=1
                return False
        except IndexError:
            self.is_end=True

    def clearPoints(self) -> None:self.wordsList[self.current_index].points = 0

    def incrementPoints(self) -> None:self.wordsList[self.current_index].points+=1

    def drawNewWord(self) -> None:
        randomNumber = rand(0, len(self.wordsList)-1)
        if len(self.wordsList)-1 !=0:
            while randomNumber == self.current_index and randomNumber <= (len(self.wordsList)-1):
                randomNumber = rand(0, len(self.wordsList)-1)
        self.current_index = randomNumber

    def setZeroAsCurrentIndex(self) -> None:self.current_index = 0

    def nextWord(self) -> None:
        self.current_index +=1
        if self.current_index > len(self.wordsList)-1:
            self.current_index = 0
    
    def previousWord(self) -> None:
        self.current_index -=1
        if self.current_index < 0:self.current_index = len(self.wordsList)-1

    def get_acquistion_level(self) -> str:
        sum_of_correct_answers=0
        for word in self.finishedWords:
            if word.mistakes == 0:sum_of_correct_answers+=2
        
        max_amount_of_points = self.neededPoints * len(self.finishedWords)
        acquistion_level = sum_of_correct_answers / max_amount_of_points

        if acquistion_level == 1:return "Celujące"
        elif acquistion_level >= 0.75 and acquistion_level < 1:return "Bardzo dobre"
        elif acquistion_level >= 0.6 and acquistion_level < 0.75:return "Dobre"
        elif acquistion_level >= 0.35 and acquistion_level < 0.6:return "Średnie"
        elif acquistion_level >= 0.2 and acquistion_level < 0.35:return "Minimalne"
        elif acquistion_level >= 0.0 and acquistion_level < 0.2:return "Zerowe"

    def empty(self):
        if len(self.wordsList) == 0:return True
        else:return False

class WordsEditor:
    
    class Word:
        def __init__(self, word_id:int, word:str, translation:str, exist_earlier:bool) -> None:
            self.word_id = word_id
            self.word = word
            self.translation = translation
            self.exist_earlier = exist_earlier
        
        def getQuery(self, topic_id:int):
            if self.exist_earlier:
                return f"UPDATE `slowka` SET `slowko`='{self.word}',`tlumaczenie`='{self.translation}' WHERE id_slowka = {self.word_id}"
            elif not self.exist_earlier:
                return f"INSERT INTO `slowka`(`slowko`, `tlumaczenie`, `id_tematu`) VALUES ('{self.word}','{self.translation}',{topic_id})"

        def get_id(self):return self.word_id

        def get_word(self):return self.word

        def get_translation(self):return self.translation


    def __init__(self, topic_id:int) -> None:
        self.topic_id = topic_id
        self.words = list()
        self.to_delete_words = list()

        query = f"SELECT id_slowka, slowko, tlumaczenie FROM slowka WHERE id_tematu = '{self.topic_id}'"
        global_variables.mycursor.execute(query)
        result = global_variables.mycursor.fetchall()
        if len(result) > 0:
            for word in result:
                self.words.append(self.Word(word[0],word[1],word[2],True))

    def is_empty(self):
        if len(self.words) == 0:
            return True
        else:
            return False

    def add_new_word(self, word, translation):
        self.words.append(self.Word(0,word,translation,False))
    
    def pop_word(self, index):
        self.to_delete_words.append(self.words[index])
        self.words.pop(index)

    def save_to_database(self):
        for word in self.words:
            global_variables.mycursor.execute(word.getQuery(self.topic_id))
        for word in self.to_delete_words:
            if word.exist_earlier:
                global_variables.mycursor.execute(f"DELETE FROM `slowka` WHERE id_slowka = {word.word_id}")
        global_variables.mydb.commit()

    def update_title(self, new_topic_name):
        query = f"UPDATE `tematy` SET `nazwa_tematu`='{new_topic_name}' WHERE `id_tematu` = {self.topic_id};"
        global_variables.mycursor.execute(query)
        global_variables.mydb.commit()

    def delete_topic(self):
        query = f"DELETE FROM slowka WHERE id_tematu={self.topic_id}"
        global_variables.mycursor.execute(query)
        query = f"DELETE FROM dane_tematow WHERE id_tematu={self.topic_id}"
        global_variables.mycursor.execute(query)
        query = f"DELETE FROM tematy WHERE id_tematu={self.topic_id}"
        global_variables.mycursor.execute(query)
        global_variables.mydb.commit()
