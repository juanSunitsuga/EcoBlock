import pygame
import sys
from model import bins, trashes, npcs, money, capacity_upgrade_cost, speed_upgrade_cost

def handle_input(player_bot, is_walkable):
    """
    Reads keyboard and mouse events to move the player bot or toggle menu/upgrades.
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_bot.move("up", is_walkable)
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_bot.move("down", is_walkable)
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_bot.move("left", is_walkable)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_bot.move("right", is_walkable)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:  # Toggle the menu with the Tab key
                global menu_open
                menu_open = not menu_open
        elif event.type == pygame.MOUSEBUTTONDOWN and menu_open:
            mouse_pos = pygame.mouse.get_pos()
            for npc in npc_list:
                if npc["upgrade_button"] and npc["upgrade_button"].collidepoint(mouse_pos):
                    if money >= 20:  # Check if the player has enough money
                        money -= 20  # Deduct the upgrade cost
                        npc["level"] += 1  # Increase the NPC's level
                        # Upgrade the NPC type if applicable
                        if npc["type"] == "non-educated" and npc["level"] >= 10:
                            npc["type"] = "normal"
                            npc["level"] = 0
                        elif npc["type"] == "normal" and npc["level"] >= 10:
                            npc["type"] = "educated"
                            npc["level"] = 10

                        # Synchronize the level and type with the corresponding NPC in the npcs list
                        for actual_npc in npcs:
                            if actual_npc.x == int(npc["location"].strip("()").split(", ")[0]) and \
                               actual_npc.y == int(npc["location"].strip("()").split(", ")[1]):
                                actual_npc.level = npc["level"]
                                actual_npc.npc_type = npc["type"]
                                break


def update_entities(player_bot):
    """
    Advances game logic for all NPCs and the player bot when menu is closed.
    """
    for npc in npcs:
        npc.move(trashes, bins)
        npc.update(trashes)
    player_bot.update(trashes, bins)


def is_walkable(x, y, tile_map):
    """
    Returns True if (x,y) is within bounds and on sidewalk or trash_bin.
    """
    return 0 <= x < len(tile_map[0]) and 0 <= y < len(tile_map) and tile_map[y][x] in ["sidewalk", "trash_bin"]


def update_npc_list(npcs):
    """
    Builds a list of dicts with name/level/location for menu rendering.
    """
    npc_list = []
    for npc in npcs:
        npc_list.append({
            "name": f"{npc.npc_type.capitalize()} NPC",
            "level": npc.level,
            "location": f"({npc.x}, {npc.y})",
            "type": npc.npc_type,
            "upgrade_button": None  # This will be updated in the menu
        })
    return npc_list


def check_game_completion(trashes, npcs, screen, WIDTH, HEIGHT):
    """
    If no trash remains and all NPCs are educated, display win message and exit.
    """
    if not trashes and all(npc.npc_type == "educated" for npc in npcs):
        font = pygame.font.SysFont(None, 48)
        win_text = font.render("Congratulations! All NPCs are educated!", True, (0, 255, 0))  # Green text
        screen.blit(win_text, (WIDTH // 2 - 300, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(5000)  # Wait for 5 seconds
        pygame.quit()
        sys.exit()