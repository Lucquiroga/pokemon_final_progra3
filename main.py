from pygame import init, mixer, display, time, draw, Rect

from controllers.combatController import CombatController
from controllers.dialogController import DialogController
from controllers.eventController import EventController
from models.menu import Menu
from models.player import Player
from utils.components import drawLife
from utils.constants import COLORS, SCREEN_SETTINGS, EVENTS
from utils.pokemons import Pikachu, Charmander, Squirtle


class Game:
    def __init__(self):
        self.__init_services()
        self.__init_window()
        self.state = 0
        self.__event_controller = EventController()
        self.__dialog_controller = DialogController()
        self.__init_player()
        self.__init_enemy()

        self.__menu = Menu(self.player, self.__event_controller, self.__dialog_controller)
        self.__menu.init()

        self.__combat_controller = CombatController(self.enemy, self.player, self.__dialog_controller, self.__menu)


    def __init_services(self):
        init()
        mixer.init()

    def __init_player(self):
        self.player = Player()
        self.player.addPokemons([Pikachu, Charmander, Squirtle])
        self.player.selected_pokemon = self.player.pokemons[0]

    def __init_enemy(self):
        self.enemy = Player()
        self.enemy.addPokemons([Pikachu, Charmander, Squirtle])
        self.enemy.selected_pokemon = self.enemy.pokemons[0]

    def __init_window(self):
        self.screen = display.set_mode((SCREEN_SETTINGS.WIDTH, SCREEN_SETTINGS.HEIGHT))
        display.set_caption(SCREEN_SETTINGS.CAPTION)
        self.clock = time.Clock()

    def __stop(self):
        self.state = 0

    def start(self):
        self.state = 1
        self.__event_controller.subscribe((EVENTS.QUIT, self.__stop))
        self.__event_controller.subscribe((EVENTS.MOVEMENT, self.__combat_controller.addMovement))

        while self.state == 1:
            self.screen.fill(COLORS.BACKGROUND)
            self.__event_controller.checkEvents()
            self.__combat_controller.runMovements()

            self.update()

            drawLife(self.screen, self.player.selected_pokemon, self.enemy.selected_pokemon)
            self.__menu.draw(self.screen)

            display.update()
            self.clock.tick(SCREEN_SETTINGS.FPS)

        self.__event_controller.unsubscribeAll()

    def update(self):
        if (self.player.selected_pokemon):
            draw.rect(self.screen, COLORS.RED, Rect(64 * 2, 600 - 128 * 2, 128, 128))

        self.__combat_controller.validateState()


if __name__ == '__main__':
    game = Game()
    game.start()
