from app.dbconnection import DBConnection

class DiscList(DBConnection):
    def __init__(self):
        super(DiscList, self).__init__('students_info.db')
        self.read_data()
        print(self.discTypes, self.discList)

    def read_data(self):
        self.discTypes = self.select(['disc_types'], ['*'], 'id_type > 8', '')
        self.discList = self.select(['disc'], ['*'], '', '')
