from dbconnection import *

class ClassDataManager:

    class ClassData:
        def __init__(self, class_id:int,class_name:str, teacher_id:int, class_code:str):
            self.class_id = class_id
            self.teacher_id = teacher_id
            self.class_name = class_name
            self.class_code = class_code

        def get_topics(self):
            query = f"SELECT * FROM tematy WHERE id_klasy={self.class_id}"
            global_variables.mycursor.execute(query)
            topicsList = list()
            for row in global_variables.mycursor.fetchall():
                topicsList.append([row[0],row[1],row[2],row[3]])
            return topicsList

        def getStudentsDataForTopic(self,topic_id) -> list():
            query = f"""SELECT  tematy.nazwa_tematu, uczniowie.login, dane_tematow.ile_ukonczen, dane_tematow.data_ostatniego_uruchomienia, dane_tematow.poziom_przyswojenia 
            FROM dane_tematow INNER JOIN uczniowie ON dane_tematow.id_ucznia=uczniowie.id_ucznia 
            INNER JOIN tematy ON dane_tematow.id_tematu=tematy.id_tematu 
            WHERE tematy.id_klasy={self.class_id} AND tematy.id_tematu={topic_id};"""
            global_variables.mycursor.execute(query)
            dataList = list()
            result = global_variables.mycursor.fetchall()
            if not len(result):
                query = f"SELECT nazwa_tematu FROM tematy WHERE id_tematu={topic_id}"
                global_variables.mycursor.execute(query)
                return global_variables.mycursor.fetchall()
            for row in result:
                date = row[3]
                acquistion_level = row[4]
                if date == None:
                    date = 'Brak danych'
                if acquistion_level == None:
                    acquistion_level = 'Brak danych'
                dataList.append([row[0],row[1],row[2],date,acquistion_level])
            return dataList

        def getAllStudentsData(self, student_id) -> list():
            query = f"""SELECT uczniowie.login, tematy.nazwa_tematu, dane_tematow.ile_ukonczen, dane_tematow.data_ostatniego_uruchomienia, dane_tematow.poziom_przyswojenia 
            FROM dane_tematow INNER JOIN uczniowie ON dane_tematow.id_ucznia=uczniowie.id_ucznia 
            INNER JOIN tematy ON dane_tematow.id_tematu=tematy.id_tematu 
            WHERE tematy.id_klasy={self.class_id} AND uczniowie.id_ucznia={student_id};"""
            global_variables.mycursor.execute(query)
            dataList = list()
            result = global_variables.mycursor.fetchall()
            if not len(result):
                query = f"SELECT login FROM uczniowie WHERE id_ucznia={student_id}"
                global_variables.mycursor.execute(query)
                return global_variables.mycursor.fetchall()
            for row in result:
                date = row[3]
                acquistion_level = row[4]
                if date == None:
                    date = 'Brak danych'
                if acquistion_level == None:
                    acquistion_level = 'Brak danych'
                dataList.append([row[0],row[1],row[2],date,acquistion_level])
            return dataList

        def getAllStudentsForClass(self) -> list():
            query = f"SELECT id_ucznia, login FROM uczniowie WHERE id_klasy={self.class_id}"
            global_variables.mycursor.execute(query)
            result = global_variables.mycursor.fetchall()
            return result

    def __init__(self, teacher_id) -> None:
        self.classDataList = list()
        query = f"SELECT * FROM klasy WHERE id_nauczyciela={teacher_id}"
        global_variables.mycursor.execute(query)
        for row in global_variables.mycursor.fetchall():
            self.classDataList.append(self.ClassData(row[0],row[1],row[2],row[3]))

