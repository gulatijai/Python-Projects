from datetime import date

from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Optional
from flask_bootstrap import Bootstrap5
from datetime import datetime

app= Flask(__name__)
bootstrap = Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class TaskTable(db.Model):
    id: Mapped[int]= mapped_column(Integer, primary_key=True)
    title: Mapped[str]= mapped_column(String(250), nullable=False)
    description: Mapped[str]=mapped_column(String(500), nullable= True)
    due_date: Mapped[str]= mapped_column(String(50), nullable=False)
    priority: Mapped[str]= mapped_column(String(50), nullable=False)
    category: Mapped[str]= mapped_column(String(50), nullable=False)
    status: Mapped[str]= mapped_column(String(50), nullable=False)
    created_date: Mapped[str]= mapped_column(String(50), nullable=False)

app.config['SECRET_KEY']= 'jaijaijai'

with app.app_context():
    db.create_all()

class TaskForm(FlaskForm):
    title= StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateField('Due Date', validators=[DataRequired()])
    priority = SelectField('Priority', choices=['Low', 'Medium', 'High'])
    category = SelectField('Category', choices=['Work', 'Personal', 'Learning'])
    submit = SubmitField('Add Task')

@app.route('/')
def index():
    todo= db.session.execute(db.select(TaskTable).where(TaskTable.status=='Todo')).scalars().all()
    in_progress= db.session.execute(db.select(TaskTable).where(TaskTable.status == 'In Progress')).scalars().all()
    done = db.session.execute(db.select(TaskTable).where(TaskTable.status == 'Done')).scalars().all()
    return render_template('index.html', todo=todo, in_progress= in_progress, done=done)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    form= TaskForm()
    if form.validate_on_submit():
        new_task= TaskTable(
            title= form.title.data,
            description= form.description.data,
            due_date= str(form.due_date.data),
            priority= form.priority.data,
            category= form.category.data,
            status= 'Todo',
            created_date= str(date.today())
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task Added Successfully','success')
        return redirect(url_for('index'))
    return render_template('add.html', form= form)

@app.route('/move/<int:task_id>/<direction>')
def move_task(task_id, direction):
    task= db.get_or_404(TaskTable, task_id)
    if direction== 'forward':
        if task.status=='Todo':
            task.status= 'In Progress'
        elif task.status=='In Progress':
            task.status='Done'
    elif direction=='backward':
        if task.status=='Done':
            task.status= 'In Progress'
        elif task.status=='In Progress':
            task.status= 'Todo'
    db.session.commit()
    flash('Task moved successfully!', 'success')

    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>',methods=['GET', 'POST'])
def edit_task(task_id):
    task= db.get_or_404(TaskTable, task_id)
    form= TaskForm(obj= task)
    if request.method == 'GET':
        form.due_date.data = datetime.strptime(task.due_date, '%Y-%m-%d').date()
    if form.validate_on_submit():
        task.title= form.title.data
        task.description= form.description.data
        task.due_date = str(form.due_date.data)
        task.priority = form.priority.data
        task.category = form.category.data

        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', form = form, task= task)

@app.route('/delete/<int:task_id>')
def delete_cafe(task_id):
    task = db.get_or_404(TaskTable, task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task Removed','danger')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)