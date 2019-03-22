
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
      db = client["myDB"]
      toonCollect = db["characters"]
      table = toonCollect.find()
      p = []
      for test in table:
        p.append(test)
      
      return Response(json_util.dumps(p), mimetype='application/json')

class Character(Resource):
    def get(self, name):
        p = calc.getCharInfo(name)
        return p
        

api.add_resource(Roster, '/roster') # Route_1
api.add_resource(Character, '/name/<name>')


if __name__ == '__main__':
     app.run(debug=False, port=GV.port)

#print('end')
