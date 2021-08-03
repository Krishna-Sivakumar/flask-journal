#!/venv/bin python3.7
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # /// is a relative path to the db file, from the main folder
db = SQLAlchemy(app)


class Posts(db.Model):
	title = db.Column(db.Text)
	text = db.Column(db.Text)
	date_posted = db.Column(db.DateTime)
	post_id = db.Column(db.Integer, primary_key=True)


if "site.db" not in os.listdir():
    db.create_all()


@app.route("/")
def index():
	return redirect("/view")


@app.route("/view")
def post():
	p = Posts.query.all()
	p = sorted(p, key=lambda x: x.date_posted, reverse=True)
	return render_template('posts.html', post= p, title="Entries")

@app.route("/add")
def add():
	return render_template('add.html',title="Add Entry")

@app.route("/process", methods=['POST'])
def process():
	if request.method == 'POST':
		form = request.form
		p = Posts(title=form['title'], text=form['text'], date_posted=datetime.now().date())
		db.session.add(p)
		db.session.commit()
		return redirect("/add")


@app.route("/<post_id>")
def view(post_id):
	p = Posts.query.get(post_id)
	return render_template('post.html', post=p, title=p.title)


@app.route("/del/<post_id>")
def delete(post_id):
	p = Posts.query.get(post_id)
	db.session.delete(p)
	db.session.commit()
	return redirect("/view")	


@app.route("/edit/<post_id>",methods = ['GET','POST'])
def edit(post_id):
	P = Posts.query.get(post_id)
	if not request.method == 'POST':
		return render_template('edit.html', post=P, title=P.title)
	else:
		form = request.form
		p = Posts.query.get(post_id)
		p.title = form['title']
		p.text = form['text']
		db.session.commit()
		return redirect('/view')


if __name__ == '__main__':
	app.run(port=5001, debug = True)
