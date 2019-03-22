import os

port = os.environ.get('PORT') or 5000
guild =os.environ.get('GUILD') or "Utopie"
server = os.environ.get('SERVER') or "Lordaeron"
mongoURL = os.environ.get('MONGO_URI')
database = os.environ.get('MONGO_DB')



#Global variables used in Gearscore calculations

scale = 1.8618;

GS_Formula_A = [
  ( 73.0000, 1.0000 ),#2
  ( 81.3750, 0.8125 ),#3
  ( 91.4500, 0.6500 ) #4
];

GS_Formula_B = [
  ( 0.0000, 2.2500 ),#1
  ( 8.0000, 2.0000 ),#2
  ( 0.7500, 1.8000 ),#3
  ( 26.000, 1.2000 ) #4
];

slotWeight = [0, 1, 0.5625, 0.75, 0, 1, 0.75, 1, 0.75, 0.5625, 0.75, 0.5625, 0.5625, 1, 1, 0.3164, 0.5625, 2, 0.3164, 0, 0, 1, 1, 1, 0, 0.3164, 0, 0, 0.3164];
