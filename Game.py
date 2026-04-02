from Model import Coin_Collection, COIN
from Board import make_board

LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"

class Game():
	lines_printed = 0

	def __init__(self):
		self.stack = []
		self.player_count = 2
		self.players = [Player(p) for p in range(self.player_count)]
		self.initiative = 0
		self.board = make_board()
		self.running = False
		self.round = 1
	
	def set_running(self, value):
		self.running = value

	def setup_round(self):
		for x in range(3):
			for player in range(self.player_count):
				p = (-(player+1) + self.initiative) % self.player_count
				self.stack.append(self.players[p].turn)
		for player in self.players:
			player.draw_up()

	def run(self):
		self.running = True
		self.setup_round()
		while self.running:
			Game.reset_printing()
			Game.print(f"Round: {self.round}")
			Game.print(self.board)
			Game.print()
			if len(self.stack) == 0:
				self.setup_round()
				self.round += 1
			self.stack.pop()()
	
	def print(s=""):
		to_print = str(s)
		print(to_print)
		Game.lines_printed += to_print.count("\n") + 1

	def input(s=""):
		input(s)
		Game.lines_printed += s.count("\n") + 1
	
	def reset_printing():
		for x in range(Game.lines_printed):
			print(LINE_UP,end=LINE_CLEAR)
		Game.lines_printed = 0

class Player():
	def __init__(self, n):
		self.hand = Coin_Collection(3)
		self.bag = Coin_Collection()
		self.bag.add_coin(COIN.ROYAL_COIN)
		self.discard_pile = Coin_Collection()
		self.supply = Coin_Collection()
		self.eliminated = Coin_Collection()
		self.name = n
	
	def draw_up(self):
		for x in range(3):
			if self.bag.size() == 0:
				if self.discard_pile.size() == 0: break
				self.discard_pile.transfer_to(self.bag)
			self.hand.add_coin(self.bag.draw_coin())
	
	def turn(self):
		Game.print(f"It's your turn, player {self.name}")
		Game.print(f"You have: {", ".join([coin for coin in self.hand])}")
		Game.input("Whatchu wanna do?")

if __name__ == "__main__":
	my_game = Game()
	my_game.run()