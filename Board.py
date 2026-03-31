class Board():
	def __init__(self):
		self.dim = {"height": 1, "width": 1}
		self.offset = {
			"x": 0, "y": 0,
			"q": 0, "r": 0
		}
		self.tiles = [[None]]
		self[self.offset["q"],self.offset["r"]] = "*"
	
	def __getitem__(self, qr):
		x, y = self.axial_to_xy(qr)
		if (
			x < 0 or x >= self.dim["width"] or
			y < 0 or y >= self.dim["height"]
			):
			raise IndexError
		return self.tiles[y][x]

	def __setitem__(self, qr, value):
		x, y = self.axial_to_xy(qr)
		if x < 0:
			for i in range(-x):
				self.offset["x"] -= 1
				for j in range(self.dim["height"]):
					self.tiles[j].insert(0,None)
				self.dim["width"] += 1
		if y < 0:
			for j in range(-y):
				self.offset["y"] -= 1
				self.tiles.insert(0, [None for i in range(self.dim["width"])])
				self.dim["height"] += 1
		if x >= self.dim["width"]:
			for i in range(x - self.dim["width"] + 1):
				for j in range(self.dim["height"]):
					self.tiles[j].append(None)
				self.dim["width"] += 1
		if y >= self.dim["height"]:
			for j in range(y - self.dim["height"] + 1):
				self.tiles.append([None for i in range(self.dim["width"])])
				self.dim["height"] += 1
		x, y = self.axial_to_xy(qr)
		self.tiles[y][x] = value

	def axial_to_xy(self, qr):
		q, r = qr
		q -= self.offset["q"]
		r -= self.offset["r"]
		parity = q&1
		col = q - self.offset["x"]
		row = r + (q - parity) // 2 - self.offset["y"]
		return (col, row)

	def xy_to_axial(self, xy):
		x, y = xy
		x -= self.offset["x"]
		y -= self.offset["y"]
		parity = x&1
		q = x - self.offset["q"]
		r = y - (x - parity) // 2 - self.offset["r"]
		return (q, r)
	
	def __str__(self):
		return "\n".join(map(lambda row: " ".join([f"{str(tile):5}" for tile in row]), self.tiles))
	
	def hexes_str(self):
		hex_width = 9
		spacing = " " * hex_width
		rows = []
		for y in range(self.dim["height"] * 2):
			rows.append([])
			parity = y&1
			true_y = y // 2
			if parity: rows[-1].append("")
			for x in range(1 if parity else 0, self.dim["width"], 2):
				# tile_rep = str(self.tiles[true_y][x])
				q, r = self.xy_to_axial((x, true_y))
				tile_rep = f"{q:^2}/{r:^2}/{-q-r:^2}"
				rows[-1].append(f"{tile_rep:>{hex_width}}")
			if parity: rows[-1].append("")

		return "\n".join([spacing.join(row) for row in rows])
	
if __name__ == "__main__":
	my_board = Board()
	for q in range(3):
		for r in range(3):
			my_board[q, r] = True
	print(my_board.hexes_str())