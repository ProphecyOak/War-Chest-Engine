from Model import Coin_Collection, COIN
from Board import make_board, Tile
from Unit import UNITS

LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"

class Game():

	def __init__(self):
		self.stack = []
		self.player_count = 2
		self.players = [Player(self, p) for p in range(self.player_count)]
		self.initiative = 0
		self.board = make_board()
		self.team_count = 2
		self.teams = [Team(n, self) for n in range(self.team_count)]
		self.teams[0].control_spots = [self.board.AxialCoordinate(0,2), self.board.AxialCoordinate(1,0)]
		self.teams[1].control_spots = [self.board.AxialCoordinate(5,6), self.board.AxialCoordinate(6,4)]
		for x in range(self.player_count):
			self.teams[x % self.team_count].add_player(self.players[x])
		self.running = False
		self.round = 1

		self.selection = {
			"coin": None,
			"spot": None
		}
	
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
		Screen.reset_printing()
		self.running = True
		self.setup_round()
		while self.running:
			if len(self.stack) == 0:
				self.setup_round()
				self.round += 1
			Screen.push_print_section()
			self.stack.pop()()
			Screen.reset_printing()
			Screen.pop_print_section()

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
		to_print = str(s) + "\n> "
		Screen.lines_printed[-1] += to_print.count("\n") + 1
		return input(to_print).lower()

	def universal_input(s):
		if s == "quit": quit()
		return s in ["back"]
	
	def await_input(s="", validator=lambda x: True):
		Screen.push_print_section()
		while True:
			value = Screen.input(s)
			Screen.reset_printing()
			if Screen.universal_input(value) or validator(value):
				Screen.pop_print_section()
				return value
	
	def reset_printing():
		for x in range(Screen.lines_printed[-1]):
			print(LINE_UP,end=LINE_CLEAR)
		Screen.lines_printed[-1] = 0

class Team():
	def __init__(self, id, game):
		self.id = id
		self.game = game
		self.control_spots = []
		self.players = []

	def add_player(self, player):
		if player.team: player.team.remove_player(player)
		self.players.append(player)
		player.team = self
	
	def remove_player(self, player):
		self.players.remove(player)
		player.team = None

	def empty_controlled_spots(self):
		options = []
		for x in self.control_spots:
			if self.game.board[x].empty(): options.append(x)
		return options
	
def valid_from_list(options):
	def validator(chosen_option):
		try:
			option_idx = int(chosen_option) - 1
			return option_idx in range(len(options))
		except:
			return chosen_option in options
	return validator

def convert_chosen(player, options, chosen_option):
	if chosen_option == "back":
		player.restart_turn()
		return
	return chosen_option if chosen_option in options else options[int(chosen_option) - 1]

class Player():
	def __init__(self, game, n):
		self.game = game
		self.units = {x: UNITS[x](self) for x in [COIN.PIKEMAN]}
		self.hand = Coin_Collection(3)
		self.bag = Coin_Collection()
		self.bag.add_coin(COIN.ROYAL_COIN)
		for unit in self.units.values():
			for x in range(2): self.bag.add_coin(unit.supply.draw_coin())
		self.discard_pile = Coin_Collection()
		self.eliminated = Coin_Collection()
		self.id = n
		self.team = None
		self.taken_initiative = False
	
	def draw_up(self):
		for x in range(3):
			if len(self.bag) == 0:
				if len(self.discard_pile) == 0: break
				self.discard_pile.transfer_to(self.bag)
			self.hand.add_coin(self.bag.draw_coin())
	
	def highlighted_hand(self, selected_coin = None):
		hand = f"You have: {", ".join([coin for coin in self.hand])}"
		if not selected_coin: return hand
		return hand.replace(selected_coin, f"\x1b[46m{selected_coin}\x1b[0m", 1)
	
	def turn(self, first_try = True):
		if first_try:
			Screen.print(f"Round: {self.game.round}{" "*30}Initiative: {self.game.initiative}")
			Screen.print(f"{self.game.board}\n\nIt's your turn, player {self.id}")
			Screen.push_print_section()
			self.game.stack.append(Screen.pop_print_section)
		else:
			Screen.print(f"Player {self.id}, try again")
		Screen.await_input("Ready? (y/yes)", lambda x: x.lower() in ["y", "yes"])
		self.game.stack.append(self.choose_coin)
	
	def restart_turn(self):
		self.game.stack.append(lambda: self.turn(False))

	def choose_coin(self):
		Screen.print(self.highlighted_hand())
			
		chosen_coin = Screen.await_input(
			"Please choose a coin:",
			valid_from_list(self.hand)
		)
		chosen_coin = convert_chosen(self, self.hand, chosen_coin)
		if not chosen_coin: return
		self.game.selection["coin"] = chosen_coin
		self.game.stack.append(lambda: self.choose_action())
	
	def elligible_actions(self, coin):
		actions = ["pass"]
		# "bolster", "move", "attack", "control", "tactic"
		for unit in self.units.values():
			if unit.can_recruit():
				actions.append("recruit")
				break
		if self.game.initiative != self.id and not self.taken_initiative: actions.append("initiative")
		if coin == COIN.ROYAL_COIN: return actions
		if self.units[coin].can_deploy(): actions.append("deploy")
		if len(self.units[coin].on_board) > 0: actions.append("bolster")
		return actions
	
	def choose_action(self):
		coin = self.game.selection["coin"]
		Screen.print(self.highlighted_hand(coin))

		actions = self.elligible_actions(coin)
		
		chosen_action = Screen.await_input(
			f"Please choose an action:\nOptions: {", ".join(actions)}",
			valid_from_list(actions)
		)
		chosen_action = convert_chosen(self, actions, chosen_action)
		if not chosen_action: return

		match chosen_action:
			case "pass":
				self.discard_coin(self.hand, coin)
			case "initiative":
				self.discard_coin(self.hand, coin)
				self.claim_initiative()
			case "recruit":
				self.game.stack.append(lambda: self.choose_recruit())
			case "deploy":
				open_spots = self.units[coin].deployable_spots()
				self.game.stack.append(lambda: self.choose_deploy(coin, open_spots))
			case "bolster":
				pass
			# case "move":
			# 	pass
			# case "attack":
			# 	pass
			# case "control":
			# 	pass
			# case "tactic":
			# 	pass

	def choose_recruit(self):
		coin_used = self.game.selection["coin"]
		Screen.print(self.highlighted_hand(coin_used))
		Screen.print("Supply: " + ", ".join([f"{name}-{len(unit.supply)}" for name, unit in self.units.items()]))

		recruitable = []
		for unit_name, unit in self.units.items():
			if unit.can_recruit():
				recruitable.append(unit_name)

		chosen_coin = Screen.await_input(
			"Please choose a unit to recruit:",
			valid_from_list(recruitable)
		)
		chosen_coin = convert_chosen(self, recruitable, chosen_coin)
		if not chosen_coin: return

		self.discard_coin(self.hand, coin_used)
		self.discard_pile.add_coin(self.units[chosen_coin].supply.draw_coin(), True)
	
	def choose_deploy(self, coin, elligible_spaces):
		Screen.print(self.highlighted_hand(coin))

		chosen_space = Screen.await_input(
			f"Please choose a space for deployment:",
			lambda space: valid_from_list(elligible_spaces)(self.game.board.string_to_axial(space))
		)
		if not chosen_space: return
		
		self.hand.remove_coin(coin)
		destination = self.game.board.string_to_axial(chosen_space)
		self.game.board[destination].coins.add_coin(coin)
		self.units[coin].on_board.append(destination)

	def claim_initiative(self):
		self.game.initiative = self.id
		self.taken_initiative = True

	def discard_coin(self, origin, coin, faceup = False):
		origin.remove_coin(coin)
		self.discard_pile.add_coin(coin, faceup)


if __name__ == "__main__":
	print()
	my_game = Game()
	my_game.run()