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
        return self.supply.size() > 0

    def can_deploy(self):
        return self.max_stacks > len(self.on_board) and len(self.deployable_spots()) > 0
    
    def can_bolster(self, id=0):
        return len(self.on_board) > 0
    
    def can_move(self, id=0):
        raise NotImplementedError
    
    def can_attack(self, id=0):
        raise NotImplementedError
    
    def can_control(self, id=0):
        raise NotImplementedError
    
    def can_tactic(self, id=0):
        raise NotImplementedError
    
    def deployable_spots(self):
        return self.player.team.empty_controlled_spots()

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
        ##  ADD NEIGHBOR OF ADJACENT HERE
        return spots

UNITS = {
    COIN.PIKEMAN: Pikeman,
    COIN.SWORDSMAN: Swordsman,
    COIN.SCOUT: Scout,
}