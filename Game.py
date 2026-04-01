from Model import Coin_Collection, COIN
from Board import make_board

class Game():
	def __init__(self):
		self.stack = []
		self.players = [Player() for p in range(2)]
		self.initiative = 0
		self.board = make_board()

class Player():
	def __init__(self):
		self.hand = Coin_Collection(3)
		self.bag = Coin_Collection()
		self.discard_pile = Coin_Collection()
		self.supply = Coin_Collection()
		self.eliminated = Coin_Collection()