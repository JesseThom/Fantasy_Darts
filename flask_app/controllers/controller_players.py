from flask import render_template, redirect, session, request, flash
from flask_app import app
import json

from flask_app.models.model_players import Player #TODO import model file here
from flask_app.models.model_teams import Team

@app.route('/player/update')
def player_update():
    if 'uuid' not in session:
        return redirect('/')
    
    # f = open('stats.json')
    # pythonanywhere location
    f = open('/home/jessethommes/Fantasy_Darts/stats.json')
    data = json.load(f)

    for i in data:
        player = Player.get_one(i)
        if not player:
            # print("-------------new player---------------")
            points = update_points(i)

            data = {
                **i,
                'player_points': points
            }
            Player.create(data)
        else:
            # print("-------------update player---------------")
            points = update_points(i)
            data= {
                **i,
                'id':player.id,
                'player_points': points
            }
            Player.update_one(data)

    update_team_points()
    return redirect('/dashboard')

# route to add player to team
@app.route("/player/add/<int:id>")
def player_add(id):
    user_id = {"id":session['uuid']}
    team = Team.get_one(user_id)
    data = {
        "teams_id": team.id,
        "id":id
            }
    # check if player is on already chosen
    temp = Player.get_one_by_id(data)
    if not temp.teams_id:
        Player.add_player_to_team(data)
        flash(f"Added {temp.first_name} {temp.last_name}","err_taken")
    else:
        flash(f"{temp.first_name} {temp.last_name} is on another team, Choose again","err_taken")

    return redirect("/my_team")

# route to remove player from team
@app.route("/player/remove/<int:id>")
def player_remove(id):
    data={'id':id}
    Player.remove_player_from_team(data)
    return redirect ("/my_team")

# update player points
def update_points(data):
    temp_points = 0
    temp_points = temp_points + (data['Whrse'] * 5)
    temp_points = temp_points + (data['Hat'] * 2.5)
    temp_points = temp_points + (data['HTon'] * 4.5)
    temp_points = temp_points + (data['LTon']* 1.5)
    temp_points = temp_points + (data['_9MR'] * 4.5)
    temp_points = temp_points + (data['_8MR'] * 4)
    temp_points = temp_points + (data['_7MR'] * 3.5)
    temp_points = temp_points + (data['_6MR'] * 3)
    temp_points = temp_points + (data['_5MR'] * 2)

    return temp_points

# update team points
def update_team_points():
    teams = Team.get_all()
    for team in teams:
        id = {'id': team.id}
        players = Player.get_all_by_team(id)
        temp_points = 0

        x=0
        for player in players:
            x = x+1
            if x == 5:
                break
            temp_points = player.player_points + temp_points

        team_points = team.team_points + temp_points
        data = {
            'id':team.id,
            'team_points': team_points,
            'team_update': temp_points
        }
        Team.update_one(data)

@app.route('/disable')
def disable():
    Team.disable_all()
    Player.reset_points()
    return redirect('/dashboard')

#route to show individual player
@app.route('/player/<int:id>')
def player_show(id):
    data = {'id': id}
    player = Player.get_one_by_id(data)
    return render_template("player_show.html", player=player)