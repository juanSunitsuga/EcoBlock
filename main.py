import pygame
import sys
from model import generate_maze, place_houses, place_trash_bins, Bot, npcs, bins, trashes
from view import load_assets, draw_map, draw_entities, draw_menu, display_stats
from controller import handle_input, update_entities, is_walkable, update_npc_list, check_game_completion

# Constants
WIDTH, HEIGHT = 832, 640
FRAME_RATE = 30

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("EcoBlock Simulator")

    # Load assets
    load_assets()

    # Initialize the game world
    generate_maze()
    place_houses()
    bins.extend(place_trash_bins())

    # Create the player-controlled bot
    player_bot = Bot(1, 1, images=None)  # TODO: Pass bot sprite dictionary

    # Game loop variables
    clock = pygame.time.Clock()
    menu_open = False
    npc_list = []

    # Main game loop
    while True:
        # Input & updates
        if not menu_open:
            handle_input(player_bot, lambda x, y: is_walkable(x, y, tile_map))
            update_entities(player_bot)
            npc_list = update_npc_list(npcs)
        else:
            handle_input(player_bot, None)

        # Render
        screen.fill((255, 255, 255))  # Clear the screen
        draw_map(screen)  # Draw the game map
        draw_entities(screen, player_bot)  # Draw the player bot and NPCs

        if menu_open:
            draw_menu(screen, npc_list)  # Draw the menu if open
        else:
            display_stats(screen, money, player_bot.capacity, player_bot.current_trash)  # Display stats
            check_game_completion(trashes, npcs)  # Check if the game is complete

        # Update the display and maintain frame rate
        pygame.display.flip()
        clock.tick(FRAME_RATE)

if __name__ == "__main__":
    main()