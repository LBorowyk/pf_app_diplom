from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, LearnPlansForm, DocumentParForm, DocumentPartsForm, UListsForm, TableForm, TableDescForm
from app.pdfcontent import pdfDefinition

@app.route('/index')
def index():
    # return "Hello, World"
    user = {'username': 'miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }, 
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    # obj = {
    #     'content': [
    #         {'text': '12345'},
    #         {'text': '67890', 'bold': 'true', 'alignment': 'center'},
    #         {'text': '123454564654564564564564564'},
    #     ]
    # }
    obj = pdfDefinition()
    print(obj.definition)
    return render_template('index.html', title="Home", user=user, posts=posts, obj=obj.definition)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('index'))
    return render_template('login.html', title="Sign In", form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/document', methods=['GET', 'POST'])
def documentdata():
    form = DocumentParForm()
    # if form.validate_on_submit():
    if form.is_submitted():
        data_id = insert_doc_data(form)
        print('insert element', data_id)
        # flash('Login requested for user {}, remember_me={}'.format(
            # form.first_str.data, form.second_str.data))
        print('submit')
        form = DocumentParForm()
        # return render_template('documentdata.html', title="Sign In", form=form)
        return redirect('/document')
    return render_template('documentdata.html', title="Sign In", form=form)

def insert_doc_data(form):
    print('insert_doc_data')
    print(form.first_str.data, form.second_str.data, form.style.data, form.documentpart.data)
    return form.insert_data_row(
        form.first_str.data,
        form.second_str.data,
        form.style.data,
        form.documentpart.data)

def get_data_id(form):
    print('form.strorradio.data', form.strorradio.data)
    if form.strorradio.data == 0:
        print('I`m hear?')
        data_id = insert_doc_data(form)['id_element']
    else:
        data_id = form.dataradiofield.data
    print(data_id)
    return data_id

@app.route('/documentparts', methods=['GET', 'POST'])
def documentparts():
    form = DocumentPartsForm()
    # if form.validate_on_submit():
    if form.is_submitted():
        print('submit')
        form.insert_doc_part()
        form = DocumentPartsForm()
        return render_template('documentparts.html', title="Sign In", form=form)
        # return redirect('/documentparts')
    return render_template('documentparts.html', title="Sign In", form=form)

def insert_li_element(data_id, ulist_id):
    UListsForm().insert_li_element(data_id, ulist_id)

@app.route('/ulists', methods=['GET', 'POST'])
def ulists():
    form = UListsForm(prefix="form")
    formdata = DocumentParForm(prefix="formdata")
    # if form.validate_on_submit():
    if form.is_submitted() and form.submit.data:
        print('submit')
        form.insert_ulist()
        return redirect('/ulists')
    if formdata.is_submitted() and formdata.submit.data:
        print('submit formdata', formdata.strorradio.data)
        data_id = get_data_id(formdata)
        print('insert element', data_id)
        insert_li_element(data_id, formdata.ulistradiofield.data)
        form = UListsForm(prefix="form")
        formdata = DocumentParForm(prefix="formdata")
        return render_template('ulists.html', title="Sign In", form=form, formdata=formdata)
    return render_template('ulists.html', title="Sign In", form=form, formdata=formdata)

@app.route('/tables', methods=['GET', 'POST'])
def tables():
    form = TableForm(profix="form")
    if form.is_submitted():
        print('submit')
        form.inserttable()
    return render_template('tables.html', title="Tables list", form=form)

@app.route('/tablesdesc', methods=['GET', 'POST'])
def tablesdesc():
    form = TableDescForm(profix="form")
    if form.is_submitted():
        print('submit')
        form.insertcell()
        form.colIndex.data = str(int(form.colIndex.data) + 1)
    return render_template('tablesdesc.html', title="Tables Cells", form=form)

@app.route('/discs', methods=['GET', 'POST'])
def learnplans():
    form = LearnPlansForm()
    return render_template('discs.html', form=form)