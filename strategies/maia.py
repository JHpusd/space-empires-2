## Calculates the shortest distance and moves along that path not caring about running into enemies. Whopp attacking it will pick the first opp
## Compatable w/ strat_plr_1
class MaiaStrat():
    def __init__(self):
        self.simple_board = {}

    def update_data(self, ship_info, mvmt):
        old_coords = ship_info['coords']
        new_coords = (old_coords[0]+mvmt[0], old_coords[1]+mvmt[1])

        self.simple_board[old_coords].remove(ship_info)

        ship_info['coords'] = new_coords

        if new_coords not in list(self.simple_board):
            self.simple_board[new_coords] = [ship_info]
        else :
            self.simple_board[new_coords].append(ship_info)

    def find_home_col(self, plr_num):
        for coord, stuff in self.simple_board.items():
            for obj in stuff :
                if obj['player_num'] == plr_num and obj['obj_type'] == 'Colony' and obj['is_home_colony']:
                    return coord

    def choose_translation(self, ship_info, choices):
        plr_num = ship_info['player_num']
        opp_plr_num = (plr_num % 2) + 1

        my_ship_coords = ship_info['coords']

        opp_home_col_coords = self.find_home_col(opp_plr_num)

        dist_sqr = (my_ship_coords[0] - opp_home_col_coords[0]) ** 2 + (my_ship_coords[1] - opp_home_col_coords[1]) ** 2
        best_mvmt = None

        for choice in choices:
            option = (choice[0] + my_ship_coords[0], choice[1] + my_ship_coords[1])
            option_dist_sqr = (option[0] - opp_home_col_coords[0]) ** 2 + (option[1] - opp_home_col_coords[1]) ** 2
            if option_dist_sqr <= dist_sqr:
                best_mvmt = choice
                dist_sqr = option_dist_sqr
        return best_mvmt

    def choose_target(self, ship, current_battle):
        plr_num = ship['player_num']

        alt_id = (plr_num % 2) + 1

        opp_ships = [ship_info for ship_info in current_battle if ship_info['player_num'] == alt_id]

        self_ships = [ship_info for ship_info in current_battle if ship_info['player_num'] == plr_num]

        return opp_ships[0]