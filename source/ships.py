from actions import Actions

class Ship(Actions):  # a ship id can either be the player or the enemy

    inventory = ["minigun", "laser", "plasma", "rocket"]
    weapon = inventory[0] if len(inventory) > 0 else ""  # (weapon equipped handle exception if inventory empty!)

    def __init__(self, identity, x, y, size, health, color, speed):
        self.identity = identity
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.health = health
        self.speed = speed
        self.fire_direction = (0, -1)
        self.move_direction = (0, -1)
