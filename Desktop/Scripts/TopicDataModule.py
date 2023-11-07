from datetime import datetime
from dbconnection import *

class TopicData:
    def __init__(self, id:int, name:str,finished_counter:int, date:str, acquistion_level:str):
        self.id = id
        self.name = name
        self.finished_counter = finished_counter
        if acquistion_level == None:
            self.acquistion_level = "Brak danych"
        else:
            self.acquistion_level = acquistion_level
        if date == None:
            self.date = "Brak danych"
        else:
            self.date = date

    def zeroWords(self):
        query = f"SELECT COUNT(id_slowka) FROM slowka WHERE id_tematu = {self.id}"
        global_variables.mycursor.execute(query)
        result = global_variables.mycursor.fetchall()

        if result[0][0] == 0:
            return True
        else:
            return False

class TopicManager:
    def __init__(self, user_id:int, class_id:int) -> None:
        self.user_id = user_id
        self.class_id = class_id
        self.topicsData = list()
        self.funtab = [self.initForGeneral, self.initForPrivate, self.initForClasses]

    def initFor(self, index:int) -> None:
        self.funtab[index]()

    def initForGeneral(self):
        self.topicsData.clear()
        self.checkforupdatesGeneral()
        query = f"SELECT tematy.id_tematu, nazwa_tematu, ile_ukonczen, data_ostatniego_uruchomienia, poziom_przyswojenia FROM dane_tematow INNER JOIN tematy ON dane_tematow.id_tematu=tematy.id_tematu WHERE dane_tematow.id_ucznia={self.user_id} AND tematy.id_ucznia IS NULL AND tematy.id_klasy IS NULL;"
        global_variables.mycursor.execute(query)
        topics = global_variables.mycursor.fetchall()
        for topic in topics:
            self.topicsData.append(TopicData(topic[0],topic[1],topic[2],topic[3],topic[4]))

    def initForPrivate(self):
        self.topicsData.clear()
        self.checkforupdatesPrivate()
        query = f"SELECT tematy.id_tematu, nazwa_tematu, ile_ukonczen, data_ostatniego_uruchomienia, poziom_przyswojenia FROM dane_tematow INNER JOIN tematy ON dane_tematow.id_tematu=tematy.id_tematu WHERE dane_tematow.id_ucznia={self.user_id} AND tematy.id_ucznia={self.user_id};"
        global_variables.mycursor.execute(query)
        topics = global_variables.mycursor.fetchall()
        for topic in topics:
            self.topicsData.append(TopicData(topic[0],topic[1],topic[2],topic[3],topic[4]))

    def initForClasses(self):
        self.topicsData.clear()
        self.checkforupdatesClasses()
        query = f"SELECT tematy.id_tematu, nazwa_tematu, ile_ukonczen, data_ostatniego_uruchomienia, poziom_przyswojenia FROM dane_tematow INNER JOIN tematy ON dane_tematow.id_tematu=tematy.id_tematu INNER JOIN uczniowie ON dane_tematow.id_ucznia=uczniowie.id_ucznia WHERE dane_tematow.id_ucznia = {self.user_id} AND tematy.id_klasy=uczniowie.id_klasy;"
        global_variables.mycursor.execute(query)
        topics = global_variables.mycursor.fetchall()
        for topic in topics:
            self.topicsData.append(TopicData(topic[0],topic[1],topic[2],topic[3],topic[4]))


    def checkforupdatesGeneral(self):
        query="SELECT tematy.id_tematu FROM tematy WHERE id_ucznia IS NULL AND id_klasy IS NULL"
        global_variables.mycursor.execute(query)
        topics_id = global_variables.mycursor.fetchall()
        for t_id in topics_id:
            query=f"SELECT id_danych FROM dane_tematow WHERE id_ucznia={self.user_id} AND id_tematu={t_id[0]}"
            global_variables.mycursor.execute(query)
            result = global_variables.mycursor.fetchall()
            if len(result)>0:
                continue
            else:
                insert = f"INSERT INTO `dane_tematow`(`id_tematu`, `id_ucznia`, `ile_ukonczen`, `data_ostatniego_uruchomienia`, `poziom_przyswojenia`) VALUES ('{t_id[0]}','{self.user_id}',0,'None', 'Brak danych')"
                global_variables.mycursor.execute(insert)
                global_variables.mydb.commit()


    def checkforupdatesPrivate(self):
        query=f"SELECT tematy.id_tematu FROM tematy WHERE id_ucznia = {self.user_id} AND id_klasy IS NULL"
        global_variables.mycursor.execute(query)
        topics_id = global_variables.mycursor.fetchall()
        for t_id in topics_id:
            query=f"SELECT id_danych FROM dane_tematow WHERE id_ucznia={self.user_id} AND id_tematu={t_id[0]}"
            global_variables.mycursor.execute(query)
            result = global_variables.mycursor.fetchall()
            if len(result)>0:
                continue
            else:
                insert = f"INSERT INTO `dane_tematow`(`id_tematu`, `id_ucznia`, `ile_ukonczen`, `data_ostatniego_uruchomienia`) VALUES ('{t_id[0]}','{self.user_id}',0,'None')"
                global_variables.mycursor.execute(insert)
                global_variables.mydb.commit()

    def checkforupdatesClasses(self):
        if self.class_id is not None:
            query=f"SELECT tematy.id_tematu FROM tematy WHERE id_ucznia IS NULL AND id_klasy = {self.class_id}"
            global_variables.mycursor.execute(query)
            topics_id = global_variables.mycursor.fetchall()
            for t_id in topics_id:
                query=f"SELECT id_danych FROM dane_tematow WHERE id_ucznia={self.user_id} AND id_tematu={t_id[0]}"
                global_variables.mycursor.execute(query)
                result = global_variables.mycursor.fetchall()
                if len(result)>0:
                    continue
                else:
                    insert = f"INSERT INTO `dane_tematow`(`id_tematu`, `id_ucznia`, `ile_ukonczen`, `data_ostatniego_uruchomienia`) VALUES ('{t_id[0]}','{self.user_id}',0,'None')"
                    global_variables.mycursor.execute(insert)
                    global_variables.mydb.commit()

    def get_data_on_id(self, id)->int:
        for data in self.topicsData:
            if data.id == id:
                return data

if __name__=="__main__":
    t = TopicManager(1)
