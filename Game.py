from Model import Coin_Collection, COIN
from Board import make_board

LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"

class Game():

	def __init__(self):
		self.stack = []
		self.player_count = 2
		self.players = [Player(self, p) for p in range(self.player_count)]
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
		Screen.print("\n"*25)
		self.running = True
		self.setup_round()
		while self.running:
			Screen.pop_print_section(True)
			Screen.reset_printing()
			Screen.print(f"Round: {self.round}")
			Screen.print(self.board)
			Screen.print()
			Screen.push_print_section()
			if len(self.stack) == 0:
				self.setup_round()
				self.round += 1
			self.stack.pop()()

class Screen():	
	lines_printed = [0]

	def push_print_section():
		Screen.lines_printed.append(0)
	
	def pop_print_section(looping = False):
		if len(Screen.lines_printed) < 2:
			if looping: return
			raise Exception("Popping root print section.")
		Screen.lines_printed[-2] += Screen.lines_printed[-1]
		Screen.lines_printed.pop()
		if looping: Screen.pop_print_section(True)

	def print(s=""):
		to_print = str(s)
		print(to_print)
		Screen.lines_printed[-1] += to_print.count("\n") + 1

	def input(s=""):
		Screen.lines_printed[-1] += s.count("\n") + 1
		return input(s)
	
	def reset_printing():
		for x in range(Screen.lines_printed[-1]):
			print(LINE_UP,end=LINE_CLEAR)
		Screen.lines_printed[-1] = 0

class Player():
	def __init__(self, game, n):
		self.game = game
		self.hand = Coin_Collection(3)
		self.bag = Coin_Collection()
		self.bag.add_coin(COIN.ROYAL_COIN)
		self.bag.add_coin(COIN.PIKEMAN)
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
	
	def highlighted_hand(self, selected_coin=""):
		hand = f"You have: {", ".join([coin for coin in self.hand])}"
		if selected_coin == "": return hand
		return hand.replace(selected_coin, f"\x1b[46m{selected_coin}\x1b[0m")
	
	def turn(self):
		Screen.print(f"It's your turn, player {self.name}")
		Screen.push_print_section() # FOR SHOWING HAND
		Screen.print(self.highlighted_hand())
		Screen.push_print_section() # FOR CHOOSING A COIN
		chosen_coin = None
		while not chosen_coin:
			Screen.print("Please select a coin:")
			coin_input = Screen.input("> ")
			Screen.reset_printing()
			if coin_input in self.hand:
				chosen_coin = coin_input
				Screen.pop_print_section() # DONE CHOOSING COIN
				break
		Screen.reset_printing()
		Screen.print(self.highlighted_hand(chosen_coin))

		Screen.input("You chose wisely...")

if __name__ == "__main__":
	my_game = Game()
	my_game.run()