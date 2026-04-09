from random import choice

class COIN():
    ROYAL_COIN = "royal coin"
    PIKEMAN = "pikeman"
    SWORDSMAN = "swordsman"
    SCOUT = "scout"

class Coin_Collection():
    def __init__(self, max_size_: int = -1):
        self._coins = []
        self._faceup = []
        self._max_size = max_size_
    
    def add_coin(self, coin: str, faceup = False):
        if self._max_size == len(self._coins):
            raise FullCollectionError
        self._coins.append(coin)
        self._faceup.append(faceup)
    
    def remove_coin(self, coin: str):
        try:
            idx = self._coins.index(coin)
            del self._coins[idx]
            del self._faceup[idx]
        except ValueError:
            raise CoinError
    
    def draw_coin(self, replacement = False):
        if len(self._coins) == 0:
            raise EmptyCollectionError
        returned_coin = choice(self._coins)
        if not replacement:
            self.remove_coin(returned_coin)
        return returned_coin
    
    def peek(self):
        return self._coins[-1]
    
    def __iter__(self):
        self._iteration_n = 0
        return self
    
    def __next__(self):
        i = self._iteration_n
        self._iteration_n += 1
        if i >= len(self._coins):
            raise StopIteration
        return self._coins[i]

    def __contains__(self, item):
        return item in self._coins
    
    def size(self):
        return len(self._coins)
    
    def transfer_to(self, other):
        for coin in self:
            other.add_coin(coin)
        self._coins.clear()
        
    
#####################################
## EXCEPTIONS
#####################################

class CoinCollectionError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class EmptyCollectionError(CoinCollectionError):
    def __init__(self, msg = "Cannot take from empty collection", *args):
        self.message = msg
        super().__init__(*args)
    
    def __str__(self):
        return f"{self.message}"

class CoinError(CoinCollectionError):
    def __init__(self, msg = "Coin not found in collection", *args):
        self.message = msg
        super().__init__(*args)
    
    def __str__(self):
        return f"{self.message}"

class FullCollectionError(CoinCollectionError):
    def __init__(self, msg = "Cannot add to full collection", *args):
        self.message = msg
        super().__init__(*args)
    
    def __str__(self):
        return f"{self.message}"