from Model import Coin_Collection, COIN
from Board import make_board

class Game():
	def __init__(self):
		self.stack = []
		self.player_count = 2
		self.players = [Player() for p in range(self.player_count)]
		self.initiative = 0
		self.board = make_board()
		self.running = False
	
	def set_running(self, value):
		self.running = value

	def setup_round(self):
		self.stack.append(lambda: self.set_running(False))
		for x in range(3):
			for player in range(self.player_count):
				p = (-(player+1) + self.initiative) % self.player_count
				self.stack.append((lambda p: lambda: print(p))(p))

	def run(self):
		self.running = True
		print(self.board)
		while self.running:
			if len(self.stack) == 0:
				self.setup_round()
			self.stack.pop()()

class Player():
	def __init__(self):
		self.hand = Coin_Collection(3)
		self.bag = Coin_Collection()
		self.discard_pile = Coin_Collection()
		self.supply = Coin_Collection()
		self.eliminated = Coin_Collection()

if __name__ == "__main__":
	my_game = Game()
	my_game.run()