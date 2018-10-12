import os
from datetime import datetime
from flask import Flask,render_template, redirect, url_for,session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])

bootstrap = Bootstrap(app)
moment = Moment(app)


#form
class CompForm(FlaskForm):
	comp = StringField('Company name', validators=[DataRequired()])
	submit = SubmitField('Check')


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
		session['comp']=form.comp.data
		comp=form.comp.data
		return redirect(url_for('index'))
	return render_template('index.html',current_time=datetime.utcnow(),form=form,comp=session.get('comp'))

@app.route('/<name>')
def user(name):
    return render_template('user.html',name=name,current_time=datetime.utcnow())



if __name__ == '__main__':
    app.run()
