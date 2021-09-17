from dataclasses import dataclass

@dataclass
class ItemData:
    title: str
    price: float
    link: str
    shipping: float = 0.00
    bid_count: int = 0

    def total_cost(self) -> float:
        return self.price + self.shipping

""" 

To be added:
shipping price,
function for total price (price+shipping)

"""