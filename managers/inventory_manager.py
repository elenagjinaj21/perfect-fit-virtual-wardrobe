class InventoryManager:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def list_items(self):
        return self.items
