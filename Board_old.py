class Board():
	DISPLAY_MODE = "FLAT"
	SHOW_COORDS = True
	HEX_SIZE = 2 if SHOW_COORDS else 1

	def __init__(self, layout_ = ""):
		self.layout = layout_
		self.load_layout()
	
	def load_layout(self):
		match self.layout:
			case "":
				self.diameter = 5
				self.radius = self.diameter//2
				self.tiles = []
				for r in range(-self.radius, self.radius + 1):
					self.tiles.append([])
					for q in range(-self.radius, self.radius + 1):
						s = - q - r
						if (
								(s < -self.radius or s > self.radius)
							):
							self.tiles[-1].append(False)
							continue
						self.tiles[-1].append(True)

	special_tiles = [(0,3)]

	def get_coord_rep(self, q, r):
		return f'{"abcdefghijklmn"[r]:>2}{str(self.diameter-q):<2} '
	
	def get_tile_rep(self, q, r):
		match Board.DISPLAY_MODE:
			case "FLAT":
				icon = "⬣" if (q, r) not in Board.special_tiles else "*"
				return (icon if not Board.SHOW_COORDS else self.get_coord_rep(q, r)) + "   "
			case "POINTY":
				return ("⬡" if not Board.SHOW_COORDS else self.get_coord_rep(q, r)) + "   "

	def __getitem__(self, id: str):
		row = self.diameter - int(id[1])
		col = "abcdefghijk".find(id[0])
		return self.tiles[row][col]
	
	def __str__(self):
		spacing_width = Board.HEX_SIZE
		match Board.DISPLAY_MODE:
			case "POINTY":
				rows = []
				for q in range(len(self.tiles)):
					rows.append(" " * q * spacing_width)
					for r in range(len(self.tiles[q])):
						r_tile = self.tiles[q][r]
						rows[-1] += self.get_tile_rep(q, r) if r_tile else "  " * spacing_width
				return "\n".join(rows)
			case "FLAT":
				out = []
				w = 1
				growing = 1
				r = self.diameter - 1
				q = 0
				for row in range(self.diameter * 2 - 1):
					out.append("  " * (self.diameter - w) * spacing_width)
					print(w)
					for x in range(w):
						r_tile = self.tiles[q][r]
						if w== 2: print(q, r)
						out[-1] += self.get_tile_rep(q,r) if r_tile else "  " * spacing_width
						r += 1
						q += 1
					q -= w
					r -= w
					if row < self.radius:
						r -= 1
						growing = 1
					elif row >= self.radius * 3:
						q += 1
						growing = -1
					else:
						r -= (row+1) % 2
						q += row % 2
						growing = -growing
					w += growing

				return "\n".join(out)

if __name__ == "__main__":
	my_board = Board()
	print(my_board)