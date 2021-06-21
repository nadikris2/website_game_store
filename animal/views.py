from re import U, X
from flask import Blueprint, app, config, render_template, request, flash, jsonify
import flask
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.sql.expression import select
from werkzeug.utils import redirect, secure_filename
from .models import *
from .models import game
from . import db
import os

views = Blueprint('views', __name__,static_folder='static')


@views.route('/', methods=['GET', 'POST'])
def home():
    data = game.query.all()
    for row in data:
        print(row.id, row.barang, row.harga, row.user_id, row.jumlah)    
        
    return render_template("index.html",data=data)


@views.route("/admin")
@login_required
@requires_roles('admin')
def admin():
    return redirect("admin/products")

@views.route('/admin/products', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def product_list():
    headings = ("ID", "Nama Barang", "Harga Barang", "Jumlah Barang", "User ID","Gambar Barang")

    data = game.query.all()

    for row in data:
        print(row.id, row.barang, row.harga, row.user_id, row.jumlah)

    return render_template("admin/products/list.html", data=data,user=current_user,headings=headings)

@views.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def products_add():
    if request.method == 'POST':
        nama_barang = request.form.get('barang')
        harga_barang = request.form.get('harga')
        jumlah_barang = request.form.get('jumlah')
        image = request.files['foto']
        
        if len(nama_barang) == 0:
            flash('Pastikan data terisi dengan benar !', category='error')
        else:
            new_game = game(barang=nama_barang,harga=harga_barang, jumlah=jumlah_barang,user_id=current_user.id)
            db.session.add(new_game)
            db.session.commit()
            tempid = new_game.id
            fileid = str(new_game.id)
            flash('Data Ditambahkan added!', category='success')
            image.filename = fileid + ".jpg"
            image.save(os.path.join("ridwan/", "static/","image/", secure_filename(image.filename)))
            new_Historygame = Historygame(id_barang=tempid, id_user=current_user.id, action="Insert")
            db.session.add(new_Historygame)
            db.session.commit()
    return render_template("admin/products/form_add.html")



@views.route('/admin/products/edit', methods=['GET','POST'])
@login_required
@requires_roles('admin')
def products_edit(): 
    id_barang = request.args.get('id')
    

    if (request.method == 'POST'):
        nama_barang = request.form.get('name')
        harga_barang = request.form.get('price')
        jumlah_barang = request.form.get('stock')
        image = request.files['foto']
        print("Edit berjalan")
        if len(nama_barang) == 0:
            flash('Pastikan data terisi dengan benar !', category='error')
        else:
            new_game = game.query.filter_by(id=id_barang).first()
            new_game.name = nama_barang
            new_game.price = harga_barang
            new_game.stock = jumlah_barang
            db.session.commit()
            fileid = str(new_game.id)
            flash('Inventory added!', category='success')
            image.filename = fileid + ".jpg"
            image.save(os.path.join("ridwan/", "static/", "images/", secure_filename(image.filename)))
            new_Historygame = Historygame(id_barang=id_barang, id_user=current_user.id, action="Insert")
            db.session.add(new_Historygame)
            db.session.commit()
                
        return redirect("/admin/products")
    
    return render_template("admin/products/form_edit.html", id_barang=id_barang) 

@views.route('/admin/products/delete', methods=['GET','POST'])
@login_required
@requires_roles('admin')
def products_delete():
    id_barang = request.args.get('id')
    deletepro = game.query.filter_by(id=id_barang).first()
    db.session.delete(deletepro)
    db.session.commit()
    new_Historygame = Historygame(id_barang=id_barang, id_user=current_user.id, action="Delete")
    db.session.add(new_Historygame)
    db.session.commit()
    return redirect("/admin/products")

@views.route('/messages', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def message():
    headings = ("Tanggal", "User", "Message") 
    data = Messages.query.all()
    if (request.method == 'POST'):
            message = request.form.get('message')
            new = Messages(nama_user=current_user.nama, message=message)
            db.session.add(new)
            db.session.commit()
            return redirect("/messages")

    return render_template("messages.html", user=current_user, headings=headings, data=data)

@views.route('/admin/cruduser', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def cruduser():
    headings = ("ID", "Nama", "Email", "Akses")
    
    data = User.query.all()

    return render_template("admin/cruduser.html", user=current_user, headings=headings, data=data)









    


