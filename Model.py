from random import choice

class COIN():
    PIKEMAN = "pikeman"

class Coin_Collection():
    def __init__(self, max_size_: int = -1):
        self._coins = []
        self._max_size = max_size_
    
    def add_coin(self, coin: str):
        if self._max_size == len(self._coins):
            raise FullCollectionError
        self._coins.append(coin)
    
    def remove_coin(self, coin: str):
        try:
            self._coins.remove(coin)
        except ValueError:
            raise CoinError
    
    def draw_coin(self, replacement = False):
        if len(self._coins) == 0:
            raise EmptyCollectionError
        returned_coin = choice(self._coins)
        if not replacement:
            self._coins.remove(returned_coin)
        return returned_coin
    
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