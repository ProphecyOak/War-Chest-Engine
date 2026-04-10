from Model import Coin_Collection, COIN
from Board import make_board, Tile
from Unit import UNITS

LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"

class Game():

	def __init__(self):
		self.stack = []
		self.player_count = 2
		units_dict = {x: UNITS[x] for x in [COIN.PIKEMAN, COIN.SCOUT]}
		player_units = [{} for x in range(self.player_count)]
		i = 0
		for name, unit in units_dict.items():
			player_units[i % self.player_count][name] = unit
			i += 1
		self.players = [Player(self, p, player_units[p]) for p in range(self.player_count)]
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

		self.selection = {}

		#TODO: Add "undo-able" toggle for unrevertable obligations
		#	Leverage this in the "Universal or" input checking
		#	Use the "allow_backsies" parameter for "await_input"
	
	def get_selection(self, field):
		return self.selection[field]

	def clear_selection(self):
		self.selection = {}
	
	def set_running(self, value):
		self.running = value

	def run(self):
		Screen.print("\n"*25)
		Screen.reset_printing()
		self.running = True
		while self.running:
			for player in self.players:
				player.draw_up()
				player.taken_initiative = self.initiative == player.id
			round_start = self.initiative
			for x in range(3):
				for i in range(self.player_count):
					player = self.players[(i+round_start) % self.player_count]
					self.stack.append(player.turn)
					Screen.push_print_section()
					while len(self.stack) > 0:
						self.stack.pop()()
						Screen.reset_printing()
					Screen.pop_print_section()
			self.round += 1

class Screen():	
	lines_printed = [0]
	indenting = False

	def push_print_section():
		Screen.lines_printed.append(0)
	
	def pop_print_section(looping = False):
		if len(Screen.lines_printed) < 2:
			if looping: return
			raise Exception("Popping root print section.")
		Screen.lines_printed[-2] += Screen.lines_printed[-1]
		Screen.lines_printed.pop()
		if looping: Screen.pop_print_section(True)
	
	def indent(s):
		if not Screen.indenting: return s
		indentation = "|   " * (len(Screen.lines_printed) - 1)
		return indentation + s.replace("\n", "\n" + indentation)

	def print(s=""):
		to_print = Screen.indent(str(s))
		print(to_print)
		Screen.lines_printed[-1] += to_print.count("\n") + 1

	def input(s=""):
		to_print = Screen.indent(str(s) + "\n> ")
		Screen.lines_printed[-1] += to_print.count("\n") + 1
		return input(to_print).lower()

	def universal_input(s, allow_backsies=True):
		if s == "quit": quit()
		if not allow_backsies: return False
		return s in ["back"]
	
	def await_input(s="", validator=lambda x: True, allow_backsies=True):
		Screen.push_print_section()
		while True:
			value = Screen.input(s)
			Screen.reset_printing()
			if Screen.universal_input(value, allow_backsies) or validator(value):
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
	def __init__(self, game, n, units):
		self.game = game
		self.units = units
		for name, unit in self.units.items():
			self.units[name] = unit(self)
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
	
	def highlighted_hand(self):
		if "coin" in self.game.selection.keys():
			selected_coin = self.game.get_selection("coin")
		else: selected_coin = None
		hand = f"In Hand: {", ".join([coin for coin in self.hand])}"
		if not selected_coin: return hand
		return hand.replace(selected_coin, f"\x1b[46m{selected_coin}\x1b[0m", 1)
	
	def turn(self, first_try = True):
		if first_try:
			Screen.print(f"Round: {self.game.round}{" "*30}Initiative: {self.game.initiative}")
			Screen.print(f"{self.game.board}\n\nIt's your turn, player {self.id}")
			Screen.push_print_section()
			self.game.stack.append(Screen.pop_print_section)
		else:
			Screen.reset_printing()
			Screen.print(f"Player {self.id}, try again")
		self.game.clear_selection()
		Screen.await_input("Ready? (y/yes)", lambda x: x.lower() in ["y", "yes"])
		if len(self.hand) == 0:
			self.game.stack.append(lambda: Screen.input("Out of coins. Mandatory pass"))
			return
		self.game.stack.append(self.choose_action)
		self.game.stack.append(lambda: self.choose_coin(self.hand))
	
	def restart_turn(self):
		self.game.stack.clear()
		self.game.stack.append(Screen.pop_print_section)
		self.game.stack.append(lambda: self.turn(False))

	def choose_coin(self, options, field="coin", purpose="", **kwargs):
		Screen.print(self.highlighted_hand())
		if "show_supply" in kwargs.keys() and kwargs["show_supply"]:
			Screen.print("Supply: " + ", ".join(
				[f"{name}-{len(unit.supply)}" for name, unit in self.units.items()]
			))
		chosen_coin = Screen.await_input(
			f"Please choose a coin{" " * (purpose != "")}{purpose}:",
			valid_from_list(options)
		)
		chosen_coin = convert_chosen(self, options, chosen_coin)
		if not chosen_coin: return
		self.game.selection[field] = chosen_coin
	
	def elligible_actions(self, coin):
		actions = ["pass"]
		# "attack", "control", "tactic"
		for unit in self.units.values():
			if unit.can_recruit():
				actions.append("recruit")
				break
		if self.game.initiative != self.id and not self.taken_initiative: actions.append("initiative")
		if coin == COIN.ROYAL_COIN: return actions
		if self.units[coin].can_deploy(): actions.append("deploy")
		if self.units[coin].can_bolster(): actions.append("bolster")
		if self.units[coin].can_move(): actions.append("move")
		if self.units[coin].can_attack(): actions.append("attack")
		return actions
	
	def choose_action(self):
		Screen.print(self.highlighted_hand())
		coin = self.game.get_selection("coin")

		actions = self.elligible_actions(coin)
		
		chosen_action = Screen.await_input(
			f"Please choose an action:\nOptions: {", ".join(actions)}",
			valid_from_list(actions)
		)
		chosen_action = convert_chosen(self, actions, chosen_action)
		if not chosen_action: return
		self.resolve_action(coin, chosen_action)

	def resolve_action(self, coin, chosen_action):
		# FACE DOWN DISCARDS
		match chosen_action:
			case "pass":
				self.discard_coin(self.hand, coin)
				return

			case "initiative":
				self.discard_coin(self.hand, coin)
				self.game.initiative = self.id
				self.taken_initiative = True
				return

			case "recruit":
				recruitable = []
				for unit_name, unit in self.units.items():
					if unit.can_recruit():
						recruitable.append(unit_name)

				def finish_recruit():
					chosen_recruit = self.game.get_selection("recruit")
					self.discard_coin(self.hand, coin)
					self.discard_pile.add_coin(self.units[chosen_recruit].supply.draw_coin(), True)

				# Screen.reset_printing()
				Screen.print("Supply: " + ", ".join([f"{name}-{len(unit.supply)}" for name, unit in self.units.items()]))
				# Screen.push_print_section(bonus=True)
				self.game.stack.append(finish_recruit)
				self.game.stack.append(lambda: self.choose_coin(
					recruitable,
					field="recruit",
					purpose="to recruit",
					show_supply=True
				))
				return
			
		# DEPLOYMENT
		match chosen_action:
			case "deploy":
				def finish_deploy():
					self.hand.remove_coin(coin)
					destination = self.game.board.string_to_axial(self.game.get_selection("space"))
					self.game.board[destination].coins.add_coin(coin)
					self.units[coin].on_board.append(destination)

				self.game.stack.append(finish_deploy)
				self.game.stack.append(lambda: self.choose_space(
					self.game.board.map_to_string(self.units[coin].deployable_spots()),
					purpose="to deploy to"
				))
				return

			case "bolster":
				def finish_bolster():
					self.hand.remove_coin(coin)
					destination = self.game.board.string_to_axial(self.game.get_selection("space"))
					self.game.board[destination].coins.add_coin(coin)

				self.game.stack.append(finish_bolster)
				self.game.stack.append(lambda: self.choose_space(
					self.units[coin].on_board,
					purpose="to bolster"
				))
				return
			
		# FACE UP DISCARDS

		if len(self.units[coin].on_board) > 1:
			pass #TODO: Append choose unit stack based on unit functions
			#		Think footman, but generalize for any number of stacks? (warship)

		stack_idx = 0 #self.game.get_selection("stack_id")
		match chosen_action:
			case "move":
				def finish_move():
					self.discard_coin(self.hand, coin, True)
					destination = self.game.board.string_to_axial(self.game.get_selection("destination"))
					original_coords = self.units[coin].on_board[stack_idx]
					new_coords = self.game.board[destination]
					self.game.board[original_coords].transfer_to(new_coords)
					self.units[coin].on_board[stack_idx] = destination

				self.game.stack.append(finish_move)
				self.game.stack.append(lambda: self.choose_space(
					self.game.board.map_to_string(self.units[coin].empty_neighbors()),
					field="destination"
				))
				return

			#TODO: Unit Attack
			case "attack":
				def finish_attack():
					self.discard_coin(self.hand, coin, True)
					target_tile = self.board[self.board.string_to_axial(self.game.get_selection("target"))]
					target_unit = target_tile.peek()
					target_tile.remove_coin(target_unit)

				
				self.game.stack.append(finish_attack)
				self.game.stack.append(lambda: self.choose_space(
					self.game.board.map_to_string(self.units[coin].attackable_neighbors(stack_idx)),
					field="target"
				))
				return

			#TODO: Unit Control
			case "control":
				raise NotImplementedError

			#TODO: Unit Tactic
			case "tactic":
				raise NotImplementedError
	
	def choose_space(self, options, field="space", purpose=""):
		Screen.print(self.highlighted_hand())
		# Screen.print(options)

		chosen_space = Screen.await_input(
			f"Please choose a space{" " * (purpose != "")}{purpose}:",
			valid_from_list(options)
		)
		chosen_space = convert_chosen(self, options, chosen_space)
		if not chosen_space: return

		self.game.selection[field] = chosen_space

	def discard_coin(self, origin, coin, faceup = False):
		origin.remove_coin(coin)
		self.discard_pile.add_coin(coin, faceup)


if __name__ == "__main__":
	print()
	my_game = Game()
	my_game.run()