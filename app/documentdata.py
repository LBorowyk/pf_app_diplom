import sqlite3
import os
import itertools

class documentData:

    def __init__(self, studid):
        # dbfilename = os.path.join('static', 'db', 'app_diplom.db')
        dbfilename = 'app_diplom.db'
        print(dbfilename)
        self.dbconn = sqlite3.connect(dbfilename)
        self.dbcursor = self.dbconn.cursor()
        self.getStartSettings()
        self.getDocumentStruct()

    def getStartSettings(self):
        sql = '''select key, value from document_desc'''
        self.dbcursor.execute(sql)
        self.docsettings = self.dbcursor.fetchall()

    def getDocumentStruct(self):
        print(self.docsettings)
        startIndex = list(filter(lambda el: el[0] == 'documentIndexPartId', self.docsettings))
        print('startIndex', startIndex)
        startIndex = startIndex.pop()[1] if len(startIndex) > 0 else 1
        print('startIndex', startIndex)
        # sql = ''' '''
        self.docStruct = self.getPartData(startIndex, {'part': 'index', 'id_part': startIndex})
        self.content = self.getPartContent(self.docStruct)
        print(self.docStruct)
        print(self.content)


    def getPartData(self, parentid, parentElement):
        sql = f''' 
            select id_part, partname from documentparts where parent_part_id={parentid} order by ord
        '''
        self.dbcursor.execute(sql)
        res = self.dbcursor.fetchall()
        parentElement['children'] = list(map(lambda el: self.getPartData(el[0], {'part': el[1], 'id_part': el[0]}), res))
        parentElement['content'] = self.read_part_data(parentid)
        return parentElement

    def getPartContent(self, parentElement):
        print('content', parentElement)
        content = parentElement['content'] if 'content' in parentElement.keys() else parentElement
        for child in parentElement['children']:
            content = [*content, *(self.getPartContent(child))]
        return content

    def form_content_element(self, element):
        funcs = {
            'caption': self.getCaption,
            'subcaption': self.getSubCaption,
            'subcaptionstrait': self.getSubSaptionstrait,
            'thtext': self.getThText,
            'text': self.getText,
            'vspace': self.getVSpace,
            'header': self.getHeader,
            'subheader': self.getSubHeader,
            'table': self.getTable,
            'ulist': self.getUList,
            'pagebreak': self.getPageBreak,
            'centertext': self.getCenterText,
            'boldright': self.getBoldRight,
            'boldcenter': self.getBoldCenter
        }
        print(element, funcs[element['style']].__name__)
        return funcs[element['style']](element['data_first'], element['data_second'])

    def read_part_data(self, partid):
        sql = f'''
        select 
            data.data_first, 
            data.data_second,
            data.ifexpression,
            styles.style
        from 
            data, 
            styles 
        where 
            data.id_part="{partid}" and 
            data.id_style=styles.id_style
        order by ord
        '''
        self.dbcursor.execute(sql)
        res = self.dbcursor.fetchall()
        print(res)
        res = list(map(lambda el: {'data_first': el[0], 'data_second': el[1], 'style': el[3]}, res))
        print(res)
        return list(itertools.chain.from_iterable(list(map(self.form_content_element, res))))

    def getElementData(self, data_id, parentElement):
        sql = f'''
        select 
            data.data_first, 
            data.data_second,
            data.ifexpression,
            styles.style
        from 
            data, 
            styles 
        where 
            data.id_element="{data_id}" and 
            data.id_style=styles.id_style
        order by ord
        '''
        self.dbcursor.execute(sql)
        res = self.dbcursor.fetchall()
        print(res)
        # parentElement['children'] = list(map(lambda el: self.getPartData(el[0], {'part': el[1], 'id_part': el[0]}), res))
        parentElement['content'] = self.read_data_element(res)
        parentElement['children'] = []
        return parentElement

    def read_data_element(self, elements):
        res = list(map(lambda el: {'data_first': el[0], 'data_second': el[1], 'style': el[3]}, elements))
        print(res)
        return list(itertools.chain.from_iterable(list(map(self.form_content_element, res))))

    def getVSpace(self, lineCount=1, fontSize=10, *args):
        return [{'text':'\n', 'fontSize': fontSize} for _ in range(int(lineCount))]
                
    def getPageBreak(self, *args):
        return [{'text': '', 'pageBreak': 'after'}]

    def getUList(self, items, *args):
        return [{
            'table': {
                'widths': [5, 7, '*'],
                'body': list(map(lambda row: ['', {'text':'–', 'alignment': 'center'}, row], items))
            },
            'layout': 'noBordersAndPaddings'
            }]
        
    def getTableRow(self, rowData):
        return list(map(lambda cell: {'text': cell}, rowData))

    def getText(self, textstr, *args):
        return [{
            'text': textstr
        }]

    def getThText(self, textstr, *args):
        return [{
            'text': textstr,
            'bold': True,
            'alignment': 'center',
            'verticalAlign': "center"
        }]

    def getCenterText(self, textstr, *args):
        return [{
            'text': textstr,
            'alignment': 'center'
        }]

    def getBoldRight(self, textstr, *args):
        return [{
            'text': textstr,
            'bold': True,
            'alignment': 'center'
        }]

    def getBoldCenter(self, textstr, *args):
        return [{
            'text': textstr,
            'bold': True,
            'alignment': 'center'
        }]

    def getStyledElement(self, text, style):
        return [{
            'text': text,
            'style': style
            }]

    def getCaption(self, text, *args):
        return self.getStyledElement(text, 'caption')

    def getSubCaption(self, text, *args):
        return self.getStyledElement(text, 'subcaption')

    def getSubSaptionstrait(self, text, *args):
        return self.getStyledElement(text, 'subcaptionstrait')

    def getHeaderElement(self, ua_str, en_str, style):
        return [{
            'table': {
                'widths': ['*'],
                 # 'headerRows': 1,
                 'body': [
                    [{
                        'text': f'{ua_str}',
                        'style': style,
                        'border': [False, False, False, True]
                    }],
                    [{
                        'text': en_str,
                        'style': style,
                        'border': [False, True, False, False]
                    }],
                ]
            },
            'layout': f'{style}Line'
        }]

    def getHeader(self, ua_str, en_str, *args):
        return [*self.getVSpace(1, 4), *self.getHeaderElement(ua_str, en_str, 'header')]

    def getSubHeader(self, ua_str, en_str, *args):
        return [*self.getVSpace(1, 4), *self.getHeaderElement(ua_str, en_str, 'subHeader')]

    def getTable(self, table_id, data_second, *args):

        sql = f''' 
        select 
            tablename,
            widthsstr,
            layout
        from 
            tables
        where 
            tables.id_table = {table_id}
        '''
        self.dbcursor.execute(sql)
        table = self.dbcursor.fetchone()

        sql = f'''
        select 
            tables_desc.rowIndex,
            tables_desc.colIndex,
            tables_desc.rowSpan,
            tables_desc.colSpan,
            tables_desc.iterable,
            tables_desc.data_id
        from 
            tables_desc
        where 
            tables_desc.id_table={table_id} 
        order by tables_desc.rowIndex, tables_desc.colIndex 
        '''
        self.dbcursor.execute(sql)
        cells = list(map(self.getCellData, self.dbcursor.fetchall()))
        print('cells', cells)
        body = self.getTableBody(cells)
        print('body', body)
        return [{
            'table': {
                'widths': self.getColumnsWidth(table[1]),
                'body': body
            },
            'layout': table[2]
        }]

    def getColumnsWidth(self, widthsstr):
        widths = list(w if w == '*' else int(w) for w in widthsstr.split(','))
        print('widths: ', widths, widthsstr)
        return widths

    def getTableBody(self, cells):
        rowCount = max(list(map(lambda el: int(el['rowIndex']), cells)))+1
        colCount = max(list(map(lambda el: int(el['colIndex']), cells)))+1
        print('rowCount', rowCount, 'colCount', colCount)
        print('cells', cells)
        # body = list(self.getCellElement(el) if el else )
        body = []
        for r in range(rowCount):
            row = []
            for c in range(colCount):
                cell = list(filter(lambda el: el['rowIndex'] == r and el['colIndex'] == c, cells))
                row.append(self.getCellElement(cell.pop()) if len(cell) > 0 else self.getEmptyCell())
            body.append(row)
        print('body:',  body)
        return body

    def getCellElement(self, cell):
        print(cell)
        cell['data'][0]['rowSpan'] = int(cell['rowSpan']) if 'rowSpan' in cell.keys() and cell['rowSpan'] != None  else 1
        cell['data'][0]['colSpan'] = int(cell['colSpan']) if 'colSpan' in cell.keys() and cell['colSpan'] != None else 1
        return cell['data']

    def getEmptyCell(self):
        return {'text': '\n'}

    def getCellData(self, el):
        data_id = el[5]
        body_struct = self.getElementData(data_id, {})
        print(body_struct)
        content = self.getPartContent(body_struct)
        return {
            'rowIndex': el[0],
            'colIndex': el[1],
            'rowSpan': el[2],
            'colSpan': el[3],
            'iterable': el[4],
            'data': content
            }

    def getUList(self, table_id, data_second, *args):
        sql = f'''
        select 
            tables_desc.rowIndex,
            tables_desc.colIndex,
            tables_desc.rowSpan,
            tables_desc.colSpan,
            tables_desc.iterable,
            tables_desc.data_id
        from 
            tables_desc
        where 
            tables_desc.id_table={table_id} 
        order by tables_desc.rowIndex, tables_desc.colIndex 
        '''
        self.dbcursor.execute(sql)
        items = list(map(lambda el: self.getCellData(el)['data'].pop(), self.dbcursor.fetchall()))
        print('cells', items)
        
        return [{
            'table': {
                'widths': [5, 7, '*'],
                'body': list(map(lambda row: ['', {'text':'–', 'alignment': 'center'}, row], items))
            },
            'layout': 'noBordersAndPaddings'
        }]

    def getPageBreak(self, *args, **kwargs):
        return [{'text': '', 'pageBreak': 'after'}]


# import sqlite3

# def dict_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return d

# con = sqlite3.connect(":memory:")
# con.row_factory = dict_factory
# cur = con.cursor()
# cur.execute("select 1 as a")
# print(cur.fetchone()["a"])