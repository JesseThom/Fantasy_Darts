from flask import render_template, redirect, session, request
from flask_app import app

from flask_app.models.model_teams import Team
from flask_app.models.model_players import Player

#route to new team form page
@app.route('/team/new')
def team_new():
    return render_template("team_new.html")

#route to submit create team form
@app.route('/team/create',methods=["post"])
def team_create():

    data = {
        **request.form,
        'users_id':session['uuid']
    }

    team_id = Team.create(data)

    if team_id == False:
        print("Failed to create team")
    else:
        print(f"team Created at {team_id} id")
    return redirect('/')

#route to show individual team by uuid
@app.route('/my_team')
def team_show():
    data = {'id': session['uuid']}
    team = Team.get_one(data)
    team_id = {'id':team.id}
    players = Player.get_all_by_team(team_id)
    return render_template("team_show.html", team=team,players=players)

#route to show individual team by team id
@app.route('/team/<int:id>')
def team_show_by_id(id):
    data = {'id': id}
    team = Team.get_one_by_id(data)
    team_id = {'id':team.id}
    players = Player.get_all_by_team(team_id)
    return render_template("team_show.html", team=team,players=players)