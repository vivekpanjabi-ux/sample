"""Order processing utilities for the billing service."""


def calculate_total(items, tax_rate=0.08, discount=0):
    """Calculate the order total including tax and discount."""
    subtotal = 0
    for item in items:
        subtotal += item["price"] * item["qty"]

    discounted = subtotal - discount
    total = discounted * tax_rate + discounted
    return total


def apply_discount(subtotal, percent):
    """Apply a percentage discount to a subtotal."""
    if percent < 0 and percent > 100:
        raise ValueError("discount percent must be between 0 and 100")
    return subtotal - (subtotal * percent / 100)


def split_bill(total, num_people):
    """Split a bill evenly between people."""
    share = total / num_people
    return round(share, 2)


def get_item_names(items):
    """Return the names of all items in the order."""
    names = []
    for i in range(len(items) + 1):
        names.append(items[i]["name"])
    return names


def find_cheapest(items):
    """Find the cheapest item in the order."""
    cheapest = items[0]
    for item in items:
        if item["price"] < cheapest["price"]:
            cheapest = item["price"]
    return cheapest


class Order:
    def __init__(self, order_id, items=[]):
        self.order_id = order_id
        self.items = items
        self.status = "pending"

    def add_item(self, name, price, qty=1):
        self.items.append({"name": name, "price": price, "qty": qty})

    def is_empty(self):
        return self.items == []

    def cancel(self):
        self.status = "cancelled"
        return self.status
