

class MenuItem:
    def __init__(self, name: str, price: float, amount: int, type: str = None):
        self.type = type
        self.name = name
        self.price = price
        self.amount = amount
    def total_price(self):
        return self.price * self.amount
    def __str__(self):
        return f"{self.name} - $ {self.price}"

class Beverage(MenuItem):
    def __init__(self, name: str, price: float, amount: int, flavour: str):
        self.type = "Beverage"
        self.flavour = flavour
        super().__init__(name, price, amount)
    def __str__(self):
        return f"{self.type} - {self.name} - {self.flavour} - $ {self.price}"


class MainCourse(MenuItem):
    def __init__(self, name: str, price: float, amount: int, appetizer: str):
        self.appetizer = appetizer
        self.type = "Main Course"
        super().__init__(name, price, amount)
    def __str__(self):
        return f"{self.type} - {self.name} - $ {self.price}"

class Hamburguer(MenuItem):
    def __init__(self, name: str, price: float, amount: int, flavour: str, size: str):
        self.size = size
        self.flavour = flavour
        self.type = "Hamburguer"
        super().__init__(name, price, amount)
    def __str__(self):
        return f"{self.type} - {self.name} - {self.flavour} - $ {self.price}"

class Pizza(MenuItem):
    def __init__(self, name: str, price: float, amount: int, flavour: str, size: str):
        self.size = size
        self.flavour = flavour
        self.type = "Pizza"
        super().__init__(name, price, amount)
    def __str__(self):
        return f"{self.type} - {self.name} - {self.flavour} - $ {self.price}"

class Salad(MenuItem):
    def __init__(self, name: str, price: float, amount: int, flavour: str, size: str):
        self.size = size
        self.flavour = flavour
        self.type = "Salad"
        super().__init__(name, price, amount)
    def __str__(self):
        return f"{self.type} - {self.name} - {self.flavour} - $ {self.price}"

class Pasta(MenuItem):
    def __init__(self, name: str, price: float, amount: int, flavour: str):
        self.flavour = flavour
        self.type = "Pasta"
        super().__init__(name, price, amount)
    def __str__(self):
        return f"{self.type} - {self.name} - {self.flavour} - $ {self.price}"

class VeganFood(MenuItem):
    def __init__(self, name: str, price: float, amount: int, flavour: str):
        self.flavour = flavour
        self.type = "Vegan"
        super().__init__(name, price, amount)
    def __str__(self):
        return f"{self.type} - {self.name} - $ {self.price}"

class SeaFood(MenuItem):
    def __init__(self, name: str, price: float, amount: int, fish_type: str):
        self.fish_type = fish_type
        self.type = "Sea Food"
        super().__init__(name, price, amount)
    def __str__(self):
        return f"{self.type} - {self.name} - $ {self.price}"

class AsianFood(MenuItem):
    def __init__(self, name: str, price: float, amount: int, flavour: str):
        self.flavour = flavour
        self.type = "Asian Food"
        super().__init__(name, price, amount)
    def __str__(self):
        return f"{self.type} - {self.name} - $ {self.price}"

class Dessert(MenuItem):
    def __init__(self, name: str, price: float, amount: int, flavour: str):
        self.flavour = flavour
        self.type = "Dessert"
        super().__init__(name, price, amount)
    def __str__(self):
        return f"{self.type} - {self.name} - $ {self.price}"

class Soup(MenuItem):
    def __init__(self, name: str, price: float, amount: int, flavour: str):
        self.flavour = flavour
        self.type = "Soup"
        super().__init__(name, price, amount)
    def __str__(self):
        return f"{self.type} - {self.name} - $ {self.price}"

class Order:
    def __init__(self, order_number: int, discount: float = 0):
        self.order_number = order_number
        self.items = []
        self.discount = discount

    def add_item(self, item: MenuItem):
        self.items.append(item)

    def remove_item(self, item: MenuItem):
        if item in self.items:
            self.items.remove(item)
        else:
            print("Item not found in the order.")

    def total_price(self) -> float:
        return sum(item.price * item.amount for item in self.items)
    
    def total_by_type(self, item_type: str) -> float:
        return sum(item.price * item.amount for item in self.items if getattr(item, 'type', None) == item_type)
    
    def count_by_type(self, item_type: str) -> int:
        return sum(item.amount for item in self.items if getattr(item, 'type', None) == item_type)
    
    def is_discounted(self) -> bool:
        # 20% si total supera 80000
        if self.total_price() > 80000:
            self.discount = self.total_price() * 0.2
            return True, "20% off total"
        # 30% en bebidas si hay más de 4 postres
        elif self.count_by_type("Dessert") > 4:
            self.discount = self.total_by_type("Beverage") * 0.3
            return True, "30% off beverages"
        # 10% en comida de mar si supera 50000
        elif self.total_by_type("Sea Food") > 50000:
            self.discount = self.total_by_type("Sea Food") * 0.1
            return True, "10% off seafood"
        else:
            self.discount = 0
            return False, "No discount"
        
    def apply_discount(self):
        if self.is_discounted():
            total = self.total_price() - self.discount
            return total, f"Discount applied: {self.discount}"
        else:
            return self.total_price(), "No discount applied"
    
    def __iter__(self):
        return OrderIterator(self)

    def __str__(self):
        order_details = f"Order Number: {self.order_number}\n"
        order_details += "Items:\n"
        for item in self:
            order_details += f"  - {item} (Amount: {item.amount})\n"
        discounted, condition = self.is_discounted()
        if discounted:
            order_details += f"Discount: {condition} (-${self.discount:.2f})\n"
            order_details += f"Total Price with Discount: {self.total_price() - self.discount:.2f}"
        else:
            order_details += f"Total Price: {self.total_price():.2f}"
        return order_details

class OrderIterator:
    def __init__(self, order: Order):
        self._order = order
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < len(self._order.items):
            item = self._order.items[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration
    