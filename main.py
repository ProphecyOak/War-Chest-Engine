from Model import *

coins = Coin_Collection(2)

for x in range(3):
    coins.add_coin(COIN.PIKEMAN)

for x in range(3):
    print(coins.draw_coin())