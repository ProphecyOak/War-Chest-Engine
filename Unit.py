from Model import Coin_Collection, COIN

class Unit():
    def __init__(self, unit_id, player, count, max_stacks):
        self.unit_id = unit_id
        self.player = player
        self.coin_total = count
        self.max_stacks = max_stacks
        self.supply = Coin_Collection()
        for x in range(self.coin_total):
            self.supply.add_coin(unit_id)
        self.on_board = []

    def can_recruit(self, id=0):
        return len(self.supply) > 0

    def can_deploy(self):
        return self.max_stacks > len(self.on_board) and len(self.deployable_spots()) > 0
    
    def can_bolster(self, id=0):
        return len(self.on_board) > id
    
    def can_move(self, id=0):
        if len(self.on_board) <= id: return False
        return len(self.empty_neighbors()) > 0
    
    def can_attack(self, id=0):
        raise NotImplementedError
    
    def can_control(self, id=0):
        raise NotImplementedError
    
    def can_tactic(self, id=0):
        raise NotImplementedError
    
    def deployable_spots(self):
        return self.map_axial_to_string(self.player.team.empty_controlled_spots())
    
    def empty_neighbors(self, id=0):
        board = self.player.game.board
        neighbors_of_stack = board.get_neighbors(self.on_board[id])
        return self.map_axial_to_string(filter(lambda coord: board[coord].empty(), neighbors_of_stack))
    
    def map_axial_to_string(self, spaces):
        return list(map(lambda x: self.player.game.board.axial_to_string(x).lower(), spaces))

class Pikeman(Unit):
    def __init__(self, player):
        super().__init__(COIN.PIKEMAN, player, 4, 1)
    
class Swordsman(Unit):
    def __init__(self, player):
        super().__init__(COIN.SWORDSMAN, player, 5, 1)
    
class Scout(Unit):
    def __init__(self, player):
        super().__init__(COIN.SCOUT, player, 5, 1)
    
    def deployable_spots(self):
        spots = self.player.team.empty_controlled_spots()
        for player in self.player.team.players:
            for unit in player.units.values():
                for stack in unit.on_board:
                    spots.extend(self.player.game.board.get_neighbors(stack))
        return self.map_axial_to_string(spots)

UNITS = {
    COIN.PIKEMAN: Pikeman,
    COIN.SWORDSMAN: Swordsman,
    COIN.SCOUT: Scout,
}