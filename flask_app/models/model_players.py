from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Player:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name =  data['last_name']
        self.LTon = data['LTon']
        self.Hat = data['Hat']
        self.Whrse = data['Whrse']
        self._9MR = data['_9MR']
        self._8MR = data['_8MR']
        self._7MR = data['_7MR']
        self._6MR = data['_6MR']
        self._5MR = data['_5MR']
        self.HTon = data['HTon']
        self.player_points = data['player_points']
        self.week = data['week']
        self.teams_id = data['teams_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#C
    @classmethod
    def create(cls,data):
        #1 query statement
        query = "INSERT INTO players (first_name, last_name, LTon, Hat, Whrse, _9MR, _8MR, _7MR, _6MR, _5MR, HTon, player_points, week) VALUES (%(first_name)s,%(last_name)s,%(LTon)s,%(Hat)s,%(Whrse)s,%(_9MR)s,%(_8MR)s,%(_7MR)s,%(_6MR)s,%(_5MR)s,%(HTon)s,%(player_points)s,%(week)s);"
        #2 contact the data
        player_id = connectToMySQL(DATABASE).query_db(query, data) 
        return player_id
#R
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM players WHERE (first_name, last_name) = (%(first_name)s,%(last_name)s);"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return False
        return cls(results[0])
    
    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM players WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM players WHERE teams_id IS NULL ORDER BY first_name;"
        # query = "SELECT * FROM players ORDER BY first_name;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_players = []
        for dict in results:
            all_players.append(cls(dict))
        return all_players
    
    @classmethod
    def get_all_by_team(cls,data):
        query = "SELECT * FROM players WHERE teams_id = %(id)s ORDER BY player_points DESC;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        all_players = []
        for dict in results:
            all_players.append(cls(dict))
        return all_players
    
    @classmethod
    def count_players(cls,data):
        query = "SELECT COUNT(*) as player_count FROM players WHERE teams_id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        # print(results[0])
        return results[0]
#U
    @classmethod
    def update_one(cls,data):
        query = "UPDATE players SET LTon = %(LTon)s,Hat =%(Hat)s,Whrse = %(Whrse)s,_9MR = %(_9MR)s,_8MR = %(_8MR)s,_7MR = %(_7MR)s,_6MR = %(_6MR)s,_5MR = %(_5MR)s,HTon = %(HTon)s,player_points = %(player_points)s,week=%(week)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def add_player_to_team(cls,data):
        query ="UPDATE players SET teams_id = %(teams_id)s WHERE (id =%(id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def remove_player_from_team(cls,data):
        query ="UPDATE players SET teams_id = NULL WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def reset_points(cls):
        query = "UPDATE players SET player_points = 0"
        return connectToMySQL(DATABASE).query_db(query)
#D
    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM players WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)