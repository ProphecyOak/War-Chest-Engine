from Model import Coin_Collection, COIN

COINS = {
    COIN.PIKEMAN: {
        "count": 4,
        "max_stacks": 1,
    },
    COIN.SWORDSMAN: {
        "count": 5,
        "max_stacks": 1,
    }
}

class Unit():
    def __init__(self, unit_id, player):
        self.player = player
        if unit_id not in COINS.keys():
            raise ValueError("Unit type not defined.")
        unit_info = COINS[unit_id]
        self.coin_total = unit_info["count"]
        self.max_stacks = unit_info["max_stacks"]
        self.supply = Coin_Collection()
        for x in range(self.coin_total):
            self.supply.add_coin(unit_id)
        self.on_board = []

    def can_recruit(self, id=0):
        return self.supply.size() > 0

    def can_deploy(self):
        return self.max_stacks > len(self.on_board) and len(self.player.team.empty_controlled_spots()) > 0
    
    def can_bolster(self, id=0):
        raise NotImplementedError
    
    def can_move(self, id=0):
        raise NotImplementedError
    
    def can_attack(self, id=0):
        raise NotImplementedError
    
    def can_control(self, id=0):
        raise NotImplementedError
    
    def can_tactic(self, id=0):
        raise NotImplementedError

    # FUNCTIONS TO CHECK DEPLOYABILITY, MOVABILITY, ETC