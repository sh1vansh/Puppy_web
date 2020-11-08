import os
from flask import Flask,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from form import Addform,Addownerform,Delform


app=Flask(__name__)
app.config['SECRET_KEY']='myseckey'

basedir= os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir,"data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
Migrate(app,db)

db.create_all()
db.session.commit()
##############################
########## models ############
##############################

class puppy(db.Model):
    __tablename__= 'puppies'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text)
    owner=db.relationship('Owner',backref='puppy',uselist=False)

    def __init__(self,name):
        self.name=name
    def __repr__(self):
        #print(self.owner)
        #return f'puppy name is {self.name} and has now owner yet'
        if self.owner:
            return f'puppy name is {self.name} having id :{self.id} and has owner {self.owner.name}'
        else:
            return f'puppy name is {self.name} having id :{self.id} and has now owner yet'
            
    
class Owner(db.Model):
    __tablename__ = 'Owner'
    id= db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text)
    puppy_id=db.Column(db.Integer,db.ForeignKey('puppies.id'))


    def __init__(self,name,puppy_id):
        self.name=name
        self.puppy_id=puppy_id
    
    def __repr__(self):
        return f'owner name is {self.name} '

###########################
####### Model ends ########
###########################

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add_pup',methods=['GET',"POST"])
def add_pup():
    form=Addform()

    if form.validate_on_submit():
        name=form.name.data
        pup=puppy(name)
        db.session.add(pup)
        db.session.commit()
        return redirect(url_for('read'))
    return render_template('add_pup.html',form=form)

@app.route('/del_pup',methods=['GET',"POST"])
def del_pup():
    form=Delform()

    if form.validate_on_submit():
        ind=form.id.data
        pup = puppy.query.get(ind)
        db.session.delete(pup)
        db.session.commit()
        return redirect(url_for('read'))
    return render_template('del_pup.html',form=form)

@app.route('/add_owner',methods=['GET',"POST"])
def add_owner():
    form=Addownerform()

    if form.validate_on_submit():
        name=form.name.data 
        puppy_id=form.puppy_id.data
        owner =Owner(name,puppy_id)
        db.session.add(owner)
        db.session.commit()
        return redirect(url_for('read'))
    return  render_template('add_owner.html',form=form)


@app.route('/read')
def read():
    pup_list=puppy.query.all()
    return render_template('read.html',lst=pup_list)
    #return render_template('read.html')

if __name__ == "__main__":
    app.run(debug=True)