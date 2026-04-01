from Model import Coin_Collection, COIN

class Board():
	HEX_WIDTH = 8
	DEFAULT_VALUE = f"{'':^{HEX_WIDTH}}"

	def __init__(self, rep_func = str):
		self.rep_func = rep_func
		self.height = 1
		self.width = 1
		self._tiles_xy = [[Board.DEFAULT_VALUE]]
		self._origin_rs = self.AxialCoordinate(0,0) #self.XYCoordinate(0,0).to_axial()
		self._origin_xy = self.XYCoordinate(0,0)
	
	def __getitem__(self, rs: Board.AxialCoordinate):
		xy = self._rs_to__true_xy(rs)
		return self._tiles_xy[xy.y][xy.x]

	def __setitem__(self, rs: Board.AxialCoordinate, value):
		xy = self._rs_to__true_xy(rs)
		self._expand_tiles(xy)
		xy = self._rs_to__true_xy(rs)
		self._tiles_xy[xy.y][xy.x] = value
	
	def _rs_to__true_xy(self, rs):
		return (rs + self._origin_rs).to_xy() + self._origin_xy

	def _expand_tiles(self, xy: Board.XYCoordinate):
		if xy.x < 0:
			xy.x -= xy.x&1
			self.width -= xy.x
			self._origin_xy.x -= xy.x
			for j in range(self.height):
				for i in range(-xy.x):
					self._tiles_xy[j].insert(0, Board.DEFAULT_VALUE)
		if xy.x >= self.width:
			self.width += xy.x - self.width + 1
			for j in range(self.height):
				self._tiles_xy[j].append(Board.DEFAULT_VALUE)
		if xy.y < 0:
			self.height -= xy.y
			self._origin_xy.y -= xy.y
			self._tiles_xy.insert(0, [Board.DEFAULT_VALUE for i in range(self.width)])
		if xy.y >= self.height:
			self.height += xy.y - self.height + 1
			self._tiles_xy.append([Board.DEFAULT_VALUE for i in range(self.width)])
	
	def __str__(self):
		return "\n".join([
			" " * ((Board.HEX_WIDTH//2 + 1) * (j%2)) + "  ".join([
				f"{self.rep_func(self._tiles_xy[j//2][i])}" for i in range(j&1, self.width, 2)
			]) for j in range(-1, -self.height*2 - 1, -1)
		])

	class AxialCoordinate():
		def __init__(self, r, s):
			self.r = r
			self.s = s
		
		def to_xy(self):
			x = self.r - self.s
			y = self.s + x // 2
			return Board.XYCoordinate(x, y)
		
		def __add__(self, other: Board.AxialCoordinate):
			return Board.AxialCoordinate(self.r + other.r, self.s + other.s)
		
		def __str__(self):
			return f"<{self.r},{self.s}>"

	class XYCoordinate():
		def __init__(self, x, y):
			self.x = x
			self.y = y
		
		def to_axial(self):
			s = self.y - self.x // 2
			r = s + self.x
			return Board.AxialCoordinate(r, s)
		
		def __add__(self, other: Board.XYCoordinate):
			return Board.XYCoordinate(self.x + other.x, self.y + other.y)
		
		def __str__(self):
			return f"({self.x},{self.y})"

class Tile():
	def __init__(self):
		self.controllable = False
		self.allegiance = -1
		self.coins = Coin_Collection()
	
	def setup(self, controllable = False, allegiance = -1):
		self.controllable = controllable
		self.allegiance = allegiance

	def __str__(self):
			colors = [
				lambda s: f"\x1b[31m{s}\x1b[0m",
				lambda s: f"\x1b[32m{s}\x1b[0m",
				lambda s: f"\x1b[34m{s}\x1b[0m",
			]
			if self.coins.size() == 0:
				hex = f"{"⬣":^{Board.HEX_WIDTH}}"
				if self.controllable: return colors[self.allegiance](hex)
				return hex
			else:
				stack = f"{self.coins.peek()[:2]}-{str(self.coins.size())}"
				label = f"{stack:^{Board.HEX_WIDTH}}"
				if self.controllable:
					return colors[self.allegiance](label)
				return label

def make_board(layout = 0):
	match layout:
		case 0:
			board = Board()
			for r in range(7):
				for s in range(7):
					rs = Board.AxialCoordinate(r,s)
					xy = rs.to_xy()
					if xy.x < -3 or xy.x > 3: continue
					board[rs] = Tile()
			control_spots = [
				(0,2,0), (1,0,0),
				(5,6,1), (6,4,1),
				(2,3), (1,4), (3,5),
				(3,1), (4,3), (5,2)
			]
			for spot in control_spots:
				rs = Board.AxialCoordinate(spot[0], spot[1])
				board[rs].setup(True, *spot[2:])
			return board

if __name__ == "__main__":
	my_board = make_board()
	my_board[Board.AxialCoordinate(1,0)].coins.add_coin(COIN.PIKEMAN)
	my_board[Board.AxialCoordinate(1,0)].coins.add_coin(COIN.PIKEMAN)
	my_board[Board.AxialCoordinate(0,2)].coins.add_coin(COIN.SWORDSMAN)
	print(my_board)