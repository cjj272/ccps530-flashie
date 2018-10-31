import os
import requests
import sys
from datetime import datetime
from flask import Flask,render_template, redirect, url_for,session,flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,RadioField
from wtforms.validators import DataRequired,Required,Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.Config')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)



#db stuff
class SummonerToAccountID(db.Model):
	__tablename__='sumtoacc'
	name = db.Column(db.String(64),primary_key=True)
	id = db.Column(db.Integer,index=True)
	def __repr__(self):
		return '<Name %r>' % self.name

#riot stuff
def GetSummonerInfo(accountName):
	r=requests.get('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + accountName,headers = {
		"X-Riot-Token": "RGAPI-44250bf4-2e19-4f3d-a81b-46afbe60a985",
	})

	if r.status_code != 200:
		return "Fail"
	return (r.json().get('name'), r.json().get('accountId'))


#form
class CompForm(FlaskForm):
	name = StringField('LoL name', validators=[DataRequired(),Length(2,15)])
	#platform = RadioField('Platform', choices=[('7','7 day'),('15','15 day'),('30','30 day')],validators=[DataRequired()])
	submit = SubmitField('Submit')


#handle 404, 500
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html',current_time=datetime.utcnow()),404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html',current_time=datetime.utcnow()),500

@app.route('/', methods=['GET','POST'])
def index():
	form=CompForm()
	if form.validate_on_submit():
		session['name']=form.name.data

		#check if user exists
		exists = SummonerToAccountID.query.filter(SummonerToAccountID.name.ilike("%"+form.name.data+"%")).first() is not None
		print(exists, file=sys.stdout)
		if exists:
			flash("User already exists",'danger')
			return redirect(url_for('index'))


		info = GetSummonerInfo(form.name.data)
		if info=="Fail":
			flash('Submit failed. User does not exist or Riot does not like us','danger')
			return redirect(url_for('index'))
		
		user = SummonerToAccountID(name=info[0],id=info[1])
		db.session.add(user)
		db.session.commit()

		flash('Success?','success')

		return redirect(url_for('index'))
	return render_template('index.html',current_time=datetime.utcnow(),form=form,name=session.get('name'),platform=session.get('platform'))

@app.route('/<name>')
def user(name):
    return render_template('user.html',name=name,current_time=datetime.utcnow())



if __name__ == '__main__':
    app.run()
