from flask import Blueprint,render_template,flash,request,url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import Deck,User,Note
from . import db
from datetime import datetime

views = Blueprint('views',__name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        return  redirect(url_for("views.dashboard"))
    else:
        return render_template("home.html",user=current_user)

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@views.route('/add_deck',methods = ["GET","POST"])
@login_required
def deck_create():
    if request.method == "POST":
        name = request.form.get("Name")
        category = request.form.get("category")
        d = Deck(name = name,title = category,user_id = current_user.id)
        db.session.add(d)
        db.session.commit()
        flash('Deck added!', category='success')
        return redirect(url_for("views.dashboard"))

    return render_template("add_deck.html",user = current_user)

@views.route('/add_card/<int:d_id>',methods = ["GET","POST"])
@login_required
def card_create(d_id):
    d = Deck.query.filter_by(d_id = d_id,user_id = current_user.id).first()
    if request.method == "POST":
        question = request.form.get("question")
        answer = request.form.get("answer")
        card = Note(front = question,back = answer,deck_id = d_id)
        db.session.add(card)
        db.session.commit()
        flash('Card added!', category='success')
        return redirect("/deck/dash/"+str(d_id))

    return render_template("add_card.html",user = current_user,data = d)


@views.route('/deck/<int:d_id>/delete')
@login_required
def delete_deck(d_id):
    d = Deck.query.filter_by(d_id = d_id,user_id = current_user.id).first()
    db.session.delete(d)
    db.session.commit()
    flash('Deck deleted successfully !',category = "success")
    return redirect(url_for("views.dashboard"))

@views.route('/deck/<action>/<int:d_id>')
@login_required
def card_dash(d_id,action):
   d = Deck.query.filter_by(d_id = d_id,user_id = current_user.id).first()
   if action == "dashboard":
      d.Score = 0
      db.session.commit()

   return render_template("card_details.html",data = d,user = current_user)

@views.route('/<int:d_id>/<int:id>/delete')
@login_required
def card_delete(id,d_id):
    c = Note.query.filter_by(id = id).first()
    db.session.delete(c)
    db.session.commit()
    flash('Card deleted successfully !',category = "success")
    return redirect("/deck/dash/"+str(d_id))

@views.route('/deck/<int:d_id>/review',methods = ["POST"])
@login_required
def card_review(d_id):
    if request.method == "POST":
        t = datetime.now()
        score = request.form.get("review")
        d = Deck.query.filter_by(d_id = d_id,user_id = current_user.id).first()
        if score:
          d.Score = d.Score + int(score)
          d.last_rev = t
          db.session.commit()
        return redirect("/deck/dash/"+str(d_id))
