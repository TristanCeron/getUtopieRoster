
from flask import Flask, Response
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson import json_util

import gsCalculations as calc
import globalVars as GV

#print('start')

app = Flask(__name__)
api = Api(app)

class Roster(Resource):
    def get(self):
      client = MongoClient(GV.mongoURL)
      db = client[GV.database]
      toonCollect = db["characters"]
      table = toonCollect.find()
      p = []
      for test in table:
        p.append(test)
      
      return Response(json_util.dumps(p), mimetype='application/json')
    
class Home(Resource):
    def get(self):
        return "Home"
    
class Icon(Resource):
    def get(self):
        return
    
class Character(Resource):
    def get(self, name):
        p = calc.getCharInfo(name)
        return p
        

api.add_resource(Roster, '/roster')
api.add_resource(Home, '/')
api.add_resource(Icon, '/favicon.ico')
api.add_resource(Character, '/name/<name>')


if __name__ == '__main__':
    app.run(debug=True, port=GV.port, host='0.0.0.0')

#print('end')
