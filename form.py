from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField

class Addform(FlaskForm):
    name=StringField('Enter puppy name: ')
    submit=SubmitField("Submit")

class Delform(FlaskForm):
    id=IntegerField("Enter puppy's id which u want to remove: ")
    submit=SubmitField("Submit")

class Addownerform(FlaskForm):
    name=StringField('Enter Owner name: ')
    puppy_id=IntegerField("Enter Puppy ID")
    submit=SubmitField("Submit")
