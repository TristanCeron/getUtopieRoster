import requests
import xml.etree.ElementTree as ET
import math
from pymongo import MongoClient
import time

import globalVars as GV

def getItemGearscore ( item, itemCollect ):

  qualityScale = 1;

  r = requests.get('https://db.rising-gods.de/?item=' + item + '&xml')

  root = ET.fromstring(r.text)

  ilvl = int(root[0][1].text)
  quality = int(root[0][2].get('id'))
  slot = int(root[0][6].get('id'))

  if quality == 5:
    qualityScale = 1.3
    quality = 4
  elif quality == 0 or quality == 1:
    qualityScale = 0.005
    quality = 2
  elif quality == 7:
    quality = 3
    ilvl = 187.05

  gs = 0

  if ilvl >= 120:
    gs = ((ilvl - GV.GS_Formula_A[quality - 2][0]) / GV.GS_Formula_A[quality - 2][1]) * GV.scale * qualityScale * GV.slotWeight[slot];
  else:
    gs = ((ilvl - GV.GS_Formula_B[quality - 1][0]) / GV.GS_Formula_B[quality - 1][1]) * GV.scale * qualityScale * GV.slotWeight[slot];
 
  if gs <= 0: 
    gs = 0

  gs = math.floor(gs)

  if slot == 17:
    gsFury = math.floor(gs/2)
  else:
    gsFury = gs

  item = {'_id': item, 'lvl': ilvl, 'gs': gs, 'gsFury': gsFury}
  itemCollect.insert_one(item)

  return item


def getCharInfo(name):
  isLoaded = False

  while isLoaded is False:
    r = requests.get("https://armory.warmane.com/api/character/" + name + "/" + GV.server + "/summary").json()
    if 'error' not in r:
      isLoaded = True
    else:
      time.sleep(0.5)
  
  
  gs = 0
  
  client = MongoClient(GV.mongoURL)
  db = client["myDB"]
  itemCollect = db["items"]

  talent = ["", ""]
  prof = ["", ""]
  skill = ["", ""]

  i = 0
  for t in r['talents']:
    talent[i] = t['tree']
    i += 1

  i = 0
  for p in r['professions']:
    prof[i] = p['name']
    skill[i] = p['skill']
    i += 1

  for equipment in r['equipment']:
    num = equipment['item']
    search = itemCollect.find_one({"_id": num})

    if search is None:
      #print(num + " pas en base de données")
      search = getItemGearscore ( num, itemCollect )
    #else:
      #print(num + " trouvé")

    if talent[0] == 'Fury' or talent[1] == 'Fury':
      gs += search['gsFury']
    else:
      gs += search['gs']

  toon = {
            "name": r['name'],
            "class": r['class'],
            "lvl": r['level'],
            "gs": gs,
            "talentA": talent[0],
            "talentB": talent[1],
            "professionA": prof[0],
            "skillA": skill[0],
            "professionB": prof[1],
            "skillB": skill[1]
          }

  return toon

def getRoster():
  r = requests.get("https://armory.warmane.com/api/guild/" + GV.guild + "/" + GV.server + "/summary").json()

  client = MongoClient(GV.mongoURL)
  db = client["myDB"]
  toonCollect = db["characters"]
  toonCollect.drop()

  for t in r['roster']:
    name = t['name']
    toon = getCharInfo(name)
    #print(toon['name'])
    toonCollect.insert_one(toon)
