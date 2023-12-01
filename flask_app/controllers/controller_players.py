from flask import render_template, redirect, session, request
from flask_app import app
import json

from flask_app.models.model_players import Player #TODO import model file here
from flask_app.models.model_teams import Team

@app.route('/player/update')
def player_update():
    if 'uuid' not in session:
        return redirect('/')
    
    f = open('stats.json')
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

    return redirect(f"/team/{team.users_id}")

# route to remove player from team
@app.route("/player/remove/<int:id>")
def player_remove(id):
    data={'id':id}
    Player.remove_player_from_team(data)
    return redirect (f"/team/{session['uuid']}")

# update player points
def update_points(data):
    temp_points = 0
    temp_points = temp_points + (data['Hat'] * 2)
    temp_points = temp_points + (data['LTon'])
    temp_points = temp_points + (data['HTon'] * 3)
    temp_points = temp_points + (data['Whrse'] * 5)
    temp_points = temp_points + (data['_9MR'] * 4)
    temp_points = temp_points + (data['_8MR'] * 3)
    temp_points = temp_points + (data['_7MR'] * 2)
    temp_points = temp_points + (data['_6MR'] * 2)
    temp_points = temp_points + (data['_5MR'])

    return temp_points

# update team points
def update_team_points():
    teams = Team.get_all()

    for team in teams:
        id = {'id': team.id}
        players = Player.get_all_by_team(id)
        temp_points = 0

        for i in range(0,4):
            print(players[i].player_points)
            temp_points = players[i].player_points + temp_points
            print(f"running {temp_points}")
        print(f"total {temp_points}")
        
        team_points = team.team_points + temp_points
        print(f"team points {team_points}")
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


# update team points
# def update_team_points():
#     teams = Team.get_all()

#     for team in teams:
#         id = {'id': team.id}
#         players = Player.get_all_by_team(id)
#         team_points = 0

#         for player in players:
#             new_points = player.player_points + team_points

#         team_points = team.team_points + new_points
#         data = {
#             'id':team.id,
#             'team_points': team_points,
#             'team_update': new_points
#         }
#         Team.update_one(data)




# not used-----------------
def update_player(data,player):
    print("-------------update player---------------")
    temp_points = 0
    temp_points = temp_points + (data['Hat'] * 2)
    temp_points = temp_points + (data['LTon'])
    temp_points = temp_points + (data['HTon'] * 3)
    temp_points = temp_points + (data['Whrse'] * 5)
    temp_points = temp_points + (data['_9MR'] * 4)
    temp_points = temp_points + (data['_8MR'] * 3)
    temp_points = temp_points + (data['_7MR'] * 2)
    temp_points = temp_points + (data['_6MR'] * 2)
    temp_points = temp_points + (data['_5MR'])

    new_data = {
        **data,
        'id': player.id,
        # 'Hat': player.Hat + data['Hat'],
        # 'LTon': player.LTon + data['LTon'],
        # 'HTon': player.HTon + data['HTon'],
        # 'Whrse': player.Whrse + data['Whrse'],
        # '_9MR': player._9MR + data['_9MR'],
        # '_8MR': player._8MR + data['_8MR'],
        # '_7MR': player._7MR + data['_7MR'],
        # '_6MR': player._6MR + data['_6MR'],
        # '_5MR': player._5MR + data['_5MR'],
        'player_points':temp_points
    }
#route to new player form page
@app.route('/player/new')
def player_new():
    return render_template("player_new.html")

#route to submit create player form
@app.route('/player/create',methods=["post"])
def player_create():
    data = request.form
    player_id = Player.create(data)
    if player_id == False:
        print("Failed to create player")
    else:
        print(f"player Created at {player_id} id")
    return redirect('/')

#route to show individual player
@app.route('/player/<int:id>')
def player_show(id):
    data = {'id': id}
    player = Player.get_one(data)
    return render_template("player_show.html", player=player)

#route to edit player form
@app.route('/player/<int:id>/edit')
def player_edit(id):
    data = {'id': id}
    player = Player.get_one(data)
    return render_template("player_edit.html", player=player)

#route to submit edit form
# @app.route('/player/<int:id>/update',methods=['post'])
# def player_update(id):
#     data = {
#         **request.form,
#         'id':id
#         }
#     Player.update_one(data)
#     return redirect('/')

#delete player route
@app.route('/player/<int:id>/delete')
def player_delete(id):
    data = {'id': id}
    Player.delete_one(data)
    return redirect("/")