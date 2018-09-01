from rnd import rnd

class Actions:  # abstract class

    x = 0
    y = 0
    fire_direction = ()
    move_direction = ()
    inventory = []
    weapon = ""
    speed = 0
    identity = ""

    def move(self, move_direction, speed):  # setter, a tuple (0,-1),(0,1),(-1,0),(1,0) to determine move_direction
        self.x += move_direction[0] * speed
        self.y += move_direction[1] * speed

    def change_fire_direction(self):  # self.direction setter, clockwise rotation (0,-1),(-1,0),(0,1),(1,0)
        self.fire_direction = (-self.fire_direction[1], self.fire_direction[0])

    def shoot(self, game):  # constructs weapon object from the blueprints based on self.weapon "string"
        if self.weapon:  # for exception handling if weapon equipped == ""
            game.create_projectile(self)
            
    def switch_weapon(self):  # setter for ship.weapon - cycle through the list over and over from 0 to end to 0
        if self.inventory:  # for exception handling if inv empty
            self.weapon = self.inventory[(self.inventory.index(self.weapon) + 1) % len(self.inventory)]

    def ai_mind(self, game):  # caller and setter
        chance = rnd(0, 100)

        if 0 < chance < 3:  # enemy moves - 1 move per frame (30 moves = 30FPS)
            self.move_direction = [(0, -1), (0, 1), (-1, 0), (1, 0)][rnd(0, 3)]
        if 0 < chance < 3:  # enemy shoots - scalable slower # 4% chance
            self.shoot(game)
        if chance == 2:  # 2% chance
            self.switch_weapon()  # enemy switches weapon - slower than shooting

        # handle direction of shooting based on relative coordinates (shoot both possible ways)
        if self.y > game.player.y and self.x > game.player.x:
            self.fire_direction = [(0, -1), (-1, 0)][rnd(0, 1)]
        if self.y < game.player.y and self.x < game.player.x:
            self.fire_direction = [(0, 1), (1, 0)][rnd(0, 1)]
        if self.y > game.player.y and self.x < game.player.x:
            self.fire_direction = [(0, -1), (1, 0)][rnd(0, 1)]
        if self.y < game.player.y and self.x > game.player.x:
            self.fire_direction = [(0, 1), (-1, 0)][rnd(0, 1)]