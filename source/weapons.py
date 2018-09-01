from actions import Actions
import colors

class Weapon(Actions):

    #  weapon blueprints are - "name": [size, color, damage, speed]
    _blueprints = {"laser": [3, colors.red, 3, 5], "plasma": [5, colors.blue, 5, 3],
                   "rocket": [8, colors.green, 10, 1], "minigun": [2, colors.yellow, 1, 10]}

    def __init__(self, name, x, y, move_direction, identity):
        self.identity = identity
        self.name = name
        self.x = x
        self.y = y
        self.size = self._blueprints[name][0]
        self.color = self._blueprints[name][1]
        self.damage = self._blueprints[name][2]
        self.speed = self._blueprints[name][3]
        self.move_direction = move_direction
