class InventoryGroup:
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        for i in self.items: # if the item is stackable
            if i.is_stackable and i.name == item.name:
                i.amount += item.amount
                return 
            
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
        if group_id == 'weapons':
            for weapon in self.groups['weapons'].items: # makes sure duplicate weapons cant be picked up
                if item.name == weapon.name: 
                    return
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
    
    def get_items(self): # all items that are not active
        items = []
        for group in self.groups:
            for item in self.groups[group].items:
                if 'active' not in item.tags:
                    items.append(item)
        return items
    
    def get_all_items(self):
        return self.groups
    
    def add_active_weapon(self, weapon):
        if weapon.is_weapon and 'active' not in weapon.tags:
            weapon.tags.append('active')
        return True
    
    def remove_active_weapon(self, weapon):
        if weapon.is_weapon and 'active' in weapon.tags:
            weapon.tags.remove('active')
    
    def sort_weapons_by_tag(self, tag):
        self.groups['weapons'].items = sorted(self.groups['weapons'].items, key=lambda x: tag not in x.tags)
            
    def get_active_weapons(self):
        weapons = []
        for item in self.get_by_tag('active'):
            if 'weapon' in item.tags:
                weapons.append(item)
        if weapons:        
            self.sort_weapons_by_tag('active')
                
        return weapons
        
            