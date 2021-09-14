from dataclasses import dataclass

@dataclass
class ItemData:
    title: str
    price: float
    link: str

""" 

To be added:
shipping price,
function for total price (price+shipping)

"""