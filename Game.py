from Model import Coin_Collection, COIN
from Board import make_board, Tile

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
			player.taken_initiative = self.initiative == player.id

	def run(self):
		Screen.print("\n"*25)
		self.running = True
		self.setup_round()
		while self.running:
			if len(self.stack) == 0:
				self.setup_round()
				self.round += 1
			Screen.pop_print_section(True)
			Screen.reset_printing()
			Screen.print(f"Round: {self.round}{" "*30}Initiative: {self.initiative}")
			Screen.print(self.board)
			Screen.print()
			Screen.push_print_section()
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
		to_print = str(s)
		Screen.lines_printed[-1] += to_print.count("\n") + 1
		return input(to_print).lower()
	
	def await_input(s="", validator=lambda x: True):
		Screen.push_print_section()
		while True:
			value = Screen.input(s)
			Screen.reset_printing()
			if validator(value):
				Screen.pop_print_section()
				return value
	
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
		self.bag.add_coin(COIN.SWORDSMAN)
		self.discard_pile = Coin_Collection()
		self.supply = Coin_Collection()
		self.eliminated = Coin_Collection()
		self.id = n
		self.taken_initiative = False
	
	def draw_up(self):
		for x in range(3):
			if self.bag.size() == 0:
				if self.discard_pile.size() == 0: break
				self.discard_pile.transfer_to(self.bag)
			self.hand.add_coin(self.bag.draw_coin())
	
	def highlighted_hand(self, selected_coin=None):
		hand = f"You have: {", ".join([coin for coin in self.hand])}"
		if not selected_coin: return hand
		return hand.replace(selected_coin, f"\x1b[46m{selected_coin}\x1b[0m")
	
	def elligible_actions(self, coin):
		actions = ["pass"]
		# "deploy", "bolster", "move", "attack", "control", "tactic"
		if self.supply.size() > 0: actions.append("recruit")
		if self.game.initiative != self.id and not self.taken_initiative: actions.append("initiative")
		return actions
	
	def turn(self):
		board = self.game.board

		def universal_input(s):
			if s == "quit": quit()
			return s in ["back"]
		def universal_or(f):
			return lambda x: universal_input(x) or f(x)
		def valid_coin(coin): return coin in self.hand
		def valid_action(actions):
			def action_in_list(action):
				try:
					action_idx = int(action) - 1
					if action_idx in range(0, len(actions)): return True
				except:
					return action in actions
				return False
			return action_in_list

		Screen.print(f"It's your turn, player {self.id}")
		Screen.push_print_section() # FOR SHOWING HAND
		chosen_coin = None
		chosen_action = None
		turn_over = False
		while not turn_over:
			Screen.print(self.highlighted_hand(chosen_coin))
			if not chosen_coin:
				chosen_coin = Screen.await_input(
					"Please choose a coin:\n> ",
					universal_or(valid_coin)
				)
				if chosen_coin == "back":
					chosen_coin = None

			elif not chosen_action:
				actions = self.elligible_actions(chosen_coin)
				chosen_action = Screen.await_input(
					f"Please choose an action:\nOptions: {", ".join(actions)}\n",
					universal_or(valid_action(actions))
				)
				if chosen_action == "back":
					chosen_coin = None
					chosen_action = None
				if chosen_action not in actions: chosen_action = actions[int(chosen_action) - 1]

			else:
				self.hand.remove_coin(chosen_coin)
				self.discard_pile.add_coin(chosen_coin)
				match chosen_action:
					case "pass" | 0:
						pass
					case "recruit" | 1:
						pass
					case "initiative" | 2:
						self.claim_initiative()
					case "deploy" | 3:
						pass
					case "bolster" | 4:
						pass
					case "move" | 5:
						pass
					case "attack" | 6:
						pass
					case "control" | 7:
						pass
					case "tactic" | 8:
						pass
				turn_over = True
			
			Screen.reset_printing()
	
	def claim_initiative(self):
		self.game.initiative = self.id
		self.taken_initiative = True


if __name__ == "__main__":
	print()
	my_game = Game()
	my_game.run()