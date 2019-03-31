from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, RadioField, FieldList, FormField, TextAreaField
from wtforms.validators import DataRequired
from werkzeug.datastructures import MultiDict
from app.fullstuddata import DiscList
from app.docdata import DocumentInfo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    language = SelectMultipleField(
        'Programming Language',
        choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
    )
    submit = SubmitField('Sign In')

class DocumentParForm(FlaskForm):
    # docinfo = DocumentInfo()
    first_str = StringField('Перший рядок')
    second_str = StringField("Другий рядок")
    submit = SubmitField('Додати рядок')
    style = RadioField(
        'Стиль рядка',
        choices = list(map(lambda el: (el['id_style'], el['style']), DocumentInfo().styles))
    )
    documentpart = RadioField(
        'Розділ документа',
        choices = list(map(lambda el: (el['id_part'], el['partname']), DocumentInfo().documentparts))
    )
    data = DocumentInfo().data
    ulistradiofield = RadioField(
            'Списки',
            choices = list(map(lambda el: (el['id_ulist'], el['ulistname']), DocumentInfo().ulists))
            )
    dataradiofield = RadioField(
        'Дані',
        choices = list(map(lambda el: (el['id_element'], f"{el['data_first']}/{el['data_second']} (style={el['id_style']}, part={el['id_part']})"), DocumentInfo().data))
    )
    strorradio = RadioField(
        'Обрати дані для заповлення',
         choices = [(0,"Створити новий елемент"), (1,'Обрати існучі дані')]
        )
    submit = SubmitField('Додати')

    
    def insert_data_row(self, data_first, data_second, id_style, id_part):
        print('id_part', id_part)
        ord = DocumentInfo().get_new_element_ord(id_part)
        print('ord', ord)
        newdata = {'data_first': data_first, 'data_second': data_second, 'id_style': id_style, 'ord': ord}
        if not id_part is None:
            newdata['id_part'] = id_part
        return DocumentInfo().insert_data_element(newdata)

class DocumentPartsForm(FlaskForm):
    partname = StringField('Назва розділу')
    parent = RadioField(
        'Розділ документа',
        choices = list(map(lambda el: (el['id_part'], el['partname']), DocumentInfo().documentparts))
    )
    partsdata = DocumentInfo().documentparts
    submit = SubmitField('Додати розділ документа')
    def insert_doc_part(self):
        DocumentInfo().insert_doc_part(self.partname.data, self.parent.data)

class UListsForm(FlaskForm):
    ulistname = StringField('Назва списку')
    lielements = TextAreaField('Елементи списку (кожен елемент -- з нового рядка)')
    ulistdata = DocumentInfo().ulists
    submit = SubmitField('Додати список')
    def insert_li_element(self, data_id, ulist_id):
        return DocumentInfo().insert_li_element(data_id, ulist_id)
    def insert_ulist(self):
        return DocumentInfo().insert_ulist(self.ulistname.data)

class TableForm(FlaskForm):
    tablename = StringField('Назва таблиці')
    widthstrs = StringField('Ширина стовпців')
    layout = RadioField(
        'Границі',
        choices=[('noBordersAndPaddings', 'без границь'), ('noPaddings', 'з границями')] 
    )
    headerrowcount = StringField('Кількість рядків заголовку')
    submit = SubmitField('Додати')
    def inserttable(self):
        DocumentInfo().inserttable(self.tablename.data, self.widthstrs.data, self.layout.data, self.headerrowcount.data)


class TableDescForm(FlaskForm):
    rowIndex = StringField('Індекс рядка')
    colIndex = StringField('Індекс стовпця')
    rowSpan = StringField('Об\'єднати рядків', default='1')
    colSpan = StringField('Об\'єднати стовпців', default='1')
    dataradiofield = RadioField(
        'Дані',
        choices = list(map(lambda el: (el['id_element'], f"{el['data_first']}/{el['data_second']} (style={el['id_style']}, part={el['id_part']})"), filter(lambda el: el['id_part'] == None or el['id_part'] == 18, DocumentInfo().data)))
    )
    tablesRadioField = RadioField(
        'Таблиця',
        choices=list(map(lambda el: (el['id_table'], el['tablename']), DocumentInfo().tables))
    )
    submit = SubmitField('Додати')

    def insertcell(self):
        DocumentInfo().insertcell(self.rowIndex.data, self.colIndex.data, self.rowSpan.data, self.colSpan.data, self.dataradiofield.data, self.tablesRadioField.data)

class DiscTypeForm(FlaskForm):
    id_type = StringField('id disc type')
    disc_name = StringField('disc type')

class DiscTypesForm(FlaskForm):
    def __init__(self, types):
        print(types)
        self.id_discs = RadioField('id disc', choices=list(map(lambda t: (t['id_type'], t['type_name']), types)))
        for type in types:
            type_data = MultiDict([('id_disc', type['id_type']), ('type_name', type['type_name'])])
            type_form = DiscTypeForm(type_data)
            self.type_names.append_entry(type_form)
        

class LearnPlansForm(FlaskForm):
    disctitle_id = StringField('Порядковий номер')#, validators=[DataRequired()])
    disctitle_ua = StringField('Назва укр')#, validators=[DataRequired()])
    disctitle_en = StringField('Назва англ')  #, validators=[DataRequired()])
    # disc_types = SelectMultipleField(
    #     'Типи дисциплін',
    #     choices = list(map(lambda dt: (dt['id_type'], dt['type_name']), DiscList().discTypes
    # )))
    
    # print('DISC_TYPES', disc_types)
    hours = StringField('Кількість годин')#, validators=[DataRequired()])
    credits = StringField('Кількість кредитів')#, validators=[DataRequired()])
    is_studied = BooleanField('Чи вивчається')
    kp_kr = StringField('КР/КП')
    id_learn_plan = StringField('id learn plan')

    def __init__(self):
        self.disc_types = DiscTypesForm(DiscList().discTypes)


