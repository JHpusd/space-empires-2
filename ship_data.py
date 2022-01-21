from ships import *

scout = {'name':"Scout",'hp':1,'atk':3,'df':0,'ship_class':"E",'cp_cost':6,'maint_cost':1}
battlecruiser = {'name':"BattleCruiser",'hp':2,'atk':5,'df':1,'ship_class':"B",'cp_cost':15,'maint_cost':2}
battleship = {'name':'Battleship','hp':3,'atk':5,'df':2,'ship_class':"A",'cp_cost':20,'maint_cost':3}
cruiser = {'name':"Cruiser",'hp':2,'atk':4,'df':1,'ship_class':"C",'cp_cost':12,'maint_cost':2}
destroyer = {'name':"Destroyer",'hp':1,'atk':4,'df':0,'ship_class':"D",'cp_cost':9,'maint_cost':1}
dreadnaught = {'name':"Dreadnaught",'hp':3,'atk':6,'df':3,'ship_class':"A",'cp_cost':24,'maint_cost':3}
all_ships = [scout, battlecruiser, battleship, cruiser, destroyer, dreadnaught]
ship_objects = {
    'Scout':Scout,
    'BattleCruiser':BattleCruiser,
    'Battleship':Battleship,
    'Cruiser':Cruiser,
    'Destroyer':Destroyer,
    'Dreadnaught':Dreadnaught}