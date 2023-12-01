from flask_app import app, bcrypt
from flask import flash, render_template, redirect, session, request

from flask_app.models.model_users import User

# register new user
@app.route('/register', methods=['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # print(pw_hash)
    data = {
        "name": request.form['name'],
        "password" : pw_hash
    }

    User.create(data)
    user = User.get_one_by_name({'name':data['name']})

    session['uuid'] = user.id
    session['name'] = user.name
    
    return redirect("/dashboard")

# login route
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    user = User.get_one_by_name({'name':data['name']})

    if not User.validate_login(data,user):
        return redirect('/')
    
    session['uuid'] = user.id
    session['name'] = user.name

    return redirect("/dashboard")

#route to new user form page
@app.route('/user/new')
def user_new():
    return render_template("user_new.html")

#route to submit create user form
@app.route('/user/create',methods=["post"])
def user_create():
    data = request.form
    user_id = User.create(data)
    if user_id == False:
        print("Failed to create user")
    else:
        print(f"User Created at {user_id} id")
    return redirect('/dashboard')



# not used------------------
#route to show individual user
@app.route('/user/<int:id>')
def user_show(id):
    data = {'id': id}
    user = User.get_one(data)
    return render_template("user_show.html", user=user)

#route to edit user form
@app.route('/user/<int:id>/edit')
def user_edit(id):
    data = {'id': id}
    user = User.get_one(data)
    return render_template("user_edit.html", user=user)

#route to submit edit form
@app.route('/user/<int:id>/update',methods=['post'])
def user_update(id):
    data = {
        **request.form,
        'id':id
        }
    User.update_one(data)
    return redirect('/')

#delete user route
@app.route('/user/<int:id>/delete')
def user_delete(id):
    data = {'id': id}
    User.delete_one(data)
    return redirect("/")