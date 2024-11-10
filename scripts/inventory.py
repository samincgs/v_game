class InventoryGroup:
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)
        
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
                  
class Inventory:
    def __init__(self):
        self.groups = {}  # dict for different inventoryGroups {'weapons' : InventoryGroup()}     

    def add_item(self, item, group_id):
        if group_id not in self.groups:
            self.groups[group_id] = InventoryGroup()
        self.groups[group_id].add_item(item)
    
    def remove_item(self, item, group_id):
        if group_id in self.groups:
            self.groups[group_id].remove_item(item)
        
    def get_group(self, group_id):
        if group_id in self.groups:
            return self.groups[group_id]
        else:
            return InventoryGroup()
    
    def get_by_tag(self, tag):
        items = []
        for group in self.groups.values():
            for item in group.items:
                if tag in item.tags:
                    items.append(item)
        return items
    
    def get_active_weapons(self):
        weapons = []
        for item in self.get_by_tag('active'):
            if 'weapon' in item.tags:
                weapons.append(item)
        return weapons
        
            