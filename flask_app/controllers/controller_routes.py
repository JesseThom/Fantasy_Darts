from flask import render_template,redirect, session
from flask_app import app

from flask_app.models.model_users import User
from flask_app.models.model_teams import Team
from flask_app.models.model_players import Player

#landing page
@app.route('/')
def landing_page():
    if 'uuid' in session:
        return redirect('/dashboard')
    
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/')
    
    # user = User.get_one({'id':session['uuid']})
    teams = Team.get_all()
    for team in teams:
        if team.users_id == session['uuid']:
            team_view = 1
            return render_template("dashboard.html",teams=teams,team_view=team_view)
    team_view = 0

    return render_template("dashboard.html",teams=teams,team_view=team_view)

@app.route('/brackets')
def brackets():
    if 'uuid' not in session:
        return redirect('/')
    
    return render_template("brackets.html")

@app.route('/scoring')
def scoring():
    if 'uuid' not in session:
        return redirect('/')
    
    return render_template("scoring.html")

@app.route('/player_list')
def player_list():
    if 'uuid' not in session:
        return redirect('/')
    
    players = Player.get_all()
    user_id = {'id':session['uuid']}
    team = Team.get_one(user_id)
    if not team:
        data= {'id':0}
        count = {'player_count':5}
    else:
        data = {'id':team.id} 
        count = Player.count_players(data)
    # print(count['player_count'])
    return render_template("player_list.html",players=players,count=count)

@app.route('/logout')
def logout():
    session.clear()
    return render_template("index.html")