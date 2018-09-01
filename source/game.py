# TODOs
# refine wall collision
# add a state machine with a menu system
# try to refactor game.methods() - update functions to properly divide responsibilities
# for the simplicity, delta-time not included (eg: if weapon.speed is bigger than ship.size, it will not register a hit)

import pygame
import colors

from rnd import rnd
from ships import Ship
from weapons import Weapon


def draw_all_objects(game):
    for category, data in game.data.items():
            for thing in data:
                pygame.draw.rect(game.screen, thing.color, (thing.x, thing.y, thing.size, thing.size))


def render_text_info(game):
    font = pygame.font.Font(None, 21)
    game.screen.blit(font.render("LEVEL: " + str(game.level), True, colors.grey), (game.width - 80, 10))
    game.screen.blit(font.render("SCORE: " + str(game.score), True, colors.grey), (game.width - 80, 25))
    game.screen.blit(font.render("WEAPON: " + str(game.player.weapon), True, colors.grey), (5, game.height - 20))
    game.screen.blit(font.render("HEALTH: " + str(game.player.health), True, colors.grey), (5, game.height - 35))


def random_color():
    return rnd(0, 255), rnd(0, 255), rnd(0, 255)


class Game:

    def start(self):
        self.build_enemy_ships("enemy", 15, self.level, colors.red, 2, self.level)
        self.gameloop()

    def __init__(self, height, width):
        pygame.init()
        self.height = height
        self.width = width
        self.fps_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.height, self.width))
        self.level = 1
        self.running = True
        self.score = 0
        self.enemy_count = 0
        self.data = {"ship": [], "weapon": []}  # all game objects references are held within this data structure
        self.player = self.build_ship("player", 300, 500, 15, 11, colors.blue, 3)

    def gameloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    if event.key == pygame.K_r:
                        self.player.shoot(self)
                    if event.key == pygame.K_w:
                        self.player.change_fire_direction()
                    if event.key == pygame.K_e:
                        self.player.switch_weapon()

            if pygame.key.get_pressed()[pygame.K_UP]:
                self.player.move((0, -1), self.player.speed)
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self.player.move((0, 1), self.player.speed)
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.player.move((-1, 0), self.player.speed)
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.player.move((1, 0), self.player.speed)

            pygame.Surface.fill(self.screen, colors.black)
            draw_all_objects(self)
            render_text_info(self)
            self.level_progression()
            self.update_data_call_all_setters()
            self.collision_detection()
            self.remove_object_references_let_garbage_collector_remove_them()
            pygame.display.update()
            self.fps_clock.tick(30)

    def collision_detection(self):
        for ship in self.data["ship"]:
            if ship.x < 0 or ship.x > self.width or ship.y < 0 or ship.y > self.height:  # wall collision all axes
                print("behind wall")  # do wall collision stuff
                ship.move_direction = (-ship.move_direction[0], -ship.move_direction[1])  # enemy ships bounce off walls
            for weapon in self.data["weapon"]:
                if weapon.x+weapon.size > ship.x and weapon.x < ship.x+ship.size:  # weapon collision x axis
                    if weapon.y+weapon.size > ship.y and weapon.y < ship.y+ship.size:  # weapon collision y axis
                        if weapon.identity != ship.identity:  # friendly fire - decide whether friend or foe
                            ship.color = random_color()
                            ship.health -= weapon.damage
                            self.data["weapon"].remove(weapon)  # do weapon collision stuff

    def remove_object_references_let_garbage_collector_remove_them(self):
        for ship in self.data["ship"]:
            if ship.health <= 0:
                self.data["ship"].remove(ship)
                if ship.identity == "enemy":
                    self.score += 1
                    self.enemy_count -= 1
        for weapon in self.data["weapon"]:
            if weapon.x < 0 or weapon.x > self.width or weapon.y < 0 or weapon.y > self.height:  # if out of game-screen, delete
                self.data["weapon"].remove(weapon)

    def update_data_call_all_setters(self):  # update game data, call methods not dependent on player interaction
        for weapon in self.data["weapon"]:  # make the weapon-projectiles move in direction
            weapon.move(weapon.move_direction, weapon.speed)  # since no weapon-move-specific function was implemented
        for ship in self.data["ship"]:  # call ai_mind() which is a collection of setters for behaviour
            if ship.identity == "enemy":
                ship.move(ship.move_direction, ship.speed)
                ship.ai_mind(self)

    def level_progression(self):
        if self.enemy_count == 0:
            self.level += 1
            self.build_enemy_ships("enemy", 15, self.level, colors.red, 2, self.level)

    def create_projectile(self, unit):
        self.data["weapon"].append(Weapon(unit.weapon, unit.x, unit.y, unit.fire_direction, unit.identity))

    def build_ship(self, identity, x, y, size, health, color, speed):
        new_player = Ship(identity, x, y, size, health, color, speed)
        self.data["ship"].append(new_player)
        return new_player

    def build_enemy_ships(self, identity, size, health, color, speed, amount):
        self.enemy_count = amount
        for number in range(amount):
            self.data["ship"].append(Ship(identity, rnd(20, 500), rnd(20, 30), size, health, color, speed))


if __name__ == '__main__':
    Game(600, 600).start()
