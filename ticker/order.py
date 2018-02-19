class Order:
    """
        Represents an order in the trade system.
    """

    def __init__(self, side="BUY", symbol="", quantity=0, price=0, postdate=""):
        self.side = side
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.postdate = postdate
