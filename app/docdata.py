from app.dbconnection import DBConnection

class DocumentInfo(DBConnection):
    def __init__(self):
        super(DocumentInfo, self).__init__('app_diplom.db')
        self.read_data()
        
    def read_data(self):
        self.styles = self.select(['styles'], ['*'], '', '')
        self.documentparts = self.select(['documentparts'], ['*'], '', ['parent_part_id', 'ord'])
        self.data = self.select(['data'], ['*'], '', '')
        self.tables = list(map(self.read_table_data, self.select(['tables', 'data'], ['*'], 'data.id_style = 10 and data.data_first = tables.id_table', '')))
        self.ulists = list(map(self.read_list_data, self.select(['tables', 'data'], ['*'], 'data.id_style = 9 and data.data_first = tables.id_table', '')))
        print(self.tables)

    def read_table_data(self, table):
        return {
            'id_table': table['id_table'],
            'tablename': table['tablename'],
        }

    def read_list_data(self, table):
        lielements = self.select(['tables_desc', 'data'], ['*'], f"tables_desc.id_table={table['id_table']} and tables_desc.data_id = data.id_element", ['tables_desc.rowIndex'])
        return {
            'id_ulist': table['id_table'],
            'ulistname': table['tablename'],
            'lielements': lielements
        }


    def insert_data_element(self, datarow):
        print('insert data element\n', datarow)
        return self.insert('data', datarow)

    def insert_li_element(self, data_id, ulist_id):
        rowIndex = self.get_next_number(
            self.select(['tables_desc'], ['rowIndex'], f'id_table = {ulist_id}', ''),
            'rowIndex'
        )
        return self.insert('tables_desc', {
            'rowIndex': rowIndex,
            'data_id': data_id,
            'id_table': ulist_id,
            'colIndex': 0,
            'rowSpan': 1,
            'colSpan': 1
            })

    def insert_ulist(self, ulistname):
        return self.insert('tables', {'tablename': ulistname})

    def get_next_number(self, array, field):
        return (max(map(lambda el: el[field], array)) if len(array) else 0) + 1

    def get_new_element_ord(self, id_part):
        print('id_part', id_part)
        return 0 if id_part is None else self.get_next_number(self.select(['data'], ['ord'], f'id_part = {id_part}', ''), 'ord')

    def insert_doc_part(self, partname, id_parent):
        print('insert_doc_part, id_parent', id_parent)
        ord = 0
        if id_parent is None:
            ord = 0
        else:
            print('Not None!!!')
            ord = self.get_next_number(self.select(['documentparts'], ['ord'], f'parent_part_id = {id_parent}', ''), 'ord')
        print('ord', ord)
        newpart = {'partname': partname, 'ord': ord}
        if not id_parent is None:
            newpart['parent_part_id'] = id_parent
        self.insert('documentparts', newpart)

    def inserttable(self, tablename, widthstrs, layout, headerrowcount):
        table = {
            'tablename': tablename,
            'widthsstr': widthstrs,
            'layout': layout,
            'headerowcount': headerrowcount
        }
        return self.insert('tables', table)

    def insertcell(self, rowIndex, colIndex, rowSpan, colSpan, data_id, id_table):
        cell = {
            'rowIndex': rowIndex,
            'colIndex': colIndex,
            'rowSpan': rowSpan,
            'colSpan': colSpan,
            'data_id': data_id,
            'id_table': id_table
        }
        return self.insert('tables_desc', cell)
