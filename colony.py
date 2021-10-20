class Colony():
    def __init__(self, player_num, coords):
        self.coords = coords
        self.player_num = player_num
        self.is_home_colony = False
        self.obj_type = "Colony"