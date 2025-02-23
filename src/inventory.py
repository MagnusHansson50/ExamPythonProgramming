import copy
from src.pickups import pickups


class Inventory:
    def __init__(self):
        self.stored_items = {}  # Dictionary att hålla reda på item och dess antal
        self.items_to_pickup_before_end = copy.deepcopy(pickups)
        print(self.items_to_pickup_before_end)

    def add_to_inventory(self, item, quantity=1):
        """Lägger till item till listan"""
        if item in self.stored_items:
            self.stored_items[item] += quantity
        else:
            self.stored_items[item] = quantity
        print(f"La till {quantity}x {item} till inventory. Total: {self.stored_items[item]}.")

    def remove_from_inventory(self, item, quantity=1):
        """Tar bort item från listan om det finns"""
        if item not in self.stored_items or self.stored_items[item] < quantity:
            print(f"Inte tillräckligt med {item} i inventory.")
            return False

        self.stored_items[item] -= quantity
        print(f"Tog bort {quantity}x {item} från inventory. Kvarvarande: {self.stored_items[item]}.")

        # Ta bort item om antalet blir 0
        if self.stored_items[item] == 0:
            del self.stored_items[item]
        return True

    def show_inventory(self):
        """Printar ut inventory"""
        print("\nInventory:")
        if not self.stored_items:
            print("Inventory är tomt.")
        for item, quantity in self.stored_items.items():
            print(f"{item}: {quantity}")

    def is_in_storage(self, item):
        """Kollar om en item finns i inventory."""
        return item in self.stored_items

    def remove_from_items_to_pickup_before_end_if_initial(self, item_to_remove):
        if item_to_remove.source == "initial":
            index = next((i for i, item in enumerate(self.items_to_pickup_before_end) if item.name == item_to_remove.name), -1)
            self.items_to_pickup_before_end.pop(index)
            length = len(self.items_to_pickup_before_end)
        if len(self.items_to_pickup_before_end) > 0:
            return False
        print("Du har hittat alla ursprungliga objekt och kan avsluta med att ta E")
        return True
