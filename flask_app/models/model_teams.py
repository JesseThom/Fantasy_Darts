from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Team:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.team_name = data['team_name']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.team_points = data['team_points']
        self.team_update = data['team_update']
        self.enable = data['enable']

#C
    @classmethod
    def create(cls,data):
        #1 query statement
        query = "INSERT INTO teams (team_name, users_id) VALUES (%(team_name)s,%(users_id)s);"
        #2 contact the data
        team_id = connectToMySQL(DATABASE).query_db(query, data) 
        return team_id
#R
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM teams WHERE users_id = %(id)s;"
        #returns list of dictionaries
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM teams ORDER BY team_points DESC;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_teams = []
        for dict in results:
            all_teams.append(cls(dict))
        return all_teams
#U
    @classmethod
    def update_one(cls,data):
        query = "UPDATE teams SET team_points = %(team_points)s,team_update =%(team_update)s,enable = 0 WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def disable_all(cls):
        query = "UPDATE teams SET team_update = 0, enable = 1;"
        return connectToMySQL(DATABASE).query_db(query)
#D
    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM teams WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)