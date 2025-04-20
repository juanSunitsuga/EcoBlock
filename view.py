import pygame
from model import TILE_SIZE, ROWS, COLS, tile_map, bins, trashes, npcs, money, capacity_upgrade_cost, speed_upgrade_cost

_assets = {}

def load_assets(path="assets/"):
    global _assets
    _assets = {
        "grass": pygame.transform.scale(pygame.image.load(path + "grass.png"), (TILE_SIZE, TILE_SIZE)),
        "sidewalk": pygame.transform.scale(pygame.image.load(path + "sidewalk.png"), (TILE_SIZE, TILE_SIZE)),
        "house": pygame.transform.scale(pygame.image.load(path + "house.png"), (TILE_SIZE, TILE_SIZE)),
        "trash_bin": pygame.transform.scale(pygame.image.load(path + "Trash Bin.png"), (TILE_SIZE, TILE_SIZE)),
    }

    # Load trash images
    _assets["trash"] = [
        pygame.transform.scale(pygame.image.load(path + "plastic-bottle.png"), (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(pygame.image.load(path + "plastic.png"), (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(pygame.image.load(path + "eaten-apple.png"), (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(pygame.image.load(path + "fishbone.png"), (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(pygame.image.load(path + "battery.png"), (TILE_SIZE, TILE_SIZE)),
    ]

    # Load bot images
    _assets["bot"] = {
        "walk": {
            "north": [
                pygame.transform.scale(pygame.image.load(path + "Playable/North 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(path + "Playable/North 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "south": [
                pygame.transform.scale(pygame.image.load(path + "Playable/South 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(path + "Playable/South 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "east": [
                pygame.transform.scale(pygame.image.load(path + "Playable/East 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(path + "Playable/East 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
            "west": [
                pygame.transform.scale(pygame.image.load(path + "Playable/West 1.png"), (TILE_SIZE, TILE_SIZE)),
                pygame.transform.scale(pygame.image.load(path + "Playable/West 2.png"), (TILE_SIZE, TILE_SIZE)),
            ],
        }
    }

    # Load NPC images
    _assets["npc"] = {
        "educated": {
            "walk": {
                "north": [
                    pygame.transform.scale(pygame.image.load(path + "Educated-NPC/North 1.png"), (TILE_SIZE, TILE_SIZE)),
                    pygame.transform.scale(pygame.image.load(path + "Educated-NPC/North 2.png"), (TILE_SIZE, TILE_SIZE)),
                ],
                "south": [
                    pygame.transform.scale(pygame.image.load(path + "Educated-NPC/South 1.png"), (TILE_SIZE, TILE_SIZE)),
                    pygame.transform.scale(pygame.image.load(path + "Educated-NPC/South 2.png"), (TILE_SIZE, TILE_SIZE)),
                ],
                "east": [
                    pygame.transform.scale(pygame.image.load(path + "Educated-NPC/East 1.png"), (TILE_SIZE, TILE_SIZE)),
                    pygame.transform.scale(pygame.image.load(path + "Educated-NPC/East 2.png"), (TILE_SIZE, TILE_SIZE)),
                ],
                "west": [
                    pygame.transform.scale(pygame.image.load(path + "Educated-NPC/West 1.png"), (TILE_SIZE, TILE_SIZE)),
                    pygame.transform.scale(pygame.image.load(path + "Educated-NPC/West 2.png"), (TILE_SIZE, TILE_SIZE)),
                ],
            }
        },
        "normal": {
            "walk": {
                "north": [
                    pygame.transform.scale(pygame.image.load(path + "Neutral-NPC/North 1.png"), (TILE_SIZE, TILE_SIZE)),
                    pygame.transform.scale(pygame.image.load(path + "Neutral-NPC/North 2.png"), (TILE_SIZE, TILE_SIZE)),
                ],
                "south": [
                    pygame.transform.scale(pygame.image.load(path + "Neutral-NPC/South 1.png"), (TILE_SIZE, TILE_SIZE)),
                    pygame.transform.scale(pygame.image.load(path + "Neutral-NPC/South 2.png"), (TILE_SIZE, TILE_SIZE)),
                ],
                "east": [
                    pygame.transform.scale(pygame.image.load(path + "Neutral-NPC/East 1.png"), (TILE_SIZE, TILE_SIZE)),
                    pygame.transform.scale(pygame.image.load(path + "Neutral-NPC/East 2.png"), (TILE_SIZE, TILE_SIZE)),
                ],
                "west": [
                    pygame.transform.scale(pygame.image.load(path + "Neutral-NPC/West 1.png"), (TILE_SIZE, TILE_SIZE)),
                    pygame.transform.scale(pygame.image.load(path + "Neutral-NPC/West 2.png"), (TILE_SIZE, TILE_SIZE)),
                ],
            }
        },
        "non-educated": {
            "walk": {
                "north": [
                    pygame.transform.scale(pygame.image.load(path + "Non-Educated-NPC/North 1.png"), (TILE_SIZE, TILE_SIZE)),
                    pygame.transform.scale(pygame.image.load(path + "Non-Educated-NPC/North 2.png"), (TILE_SIZE, TILE_SIZE)),
                ],
                "south": [
                    pygame.transform.scale(pygame.image.load(path + "Non-Educated-NPC/South 1.png"), (TILE_SIZE, TILE_SIZE)),
                    pygame.transform.scale(pygame.image.load(path + "Non-Educated-NPC/South 2.png"), (TILE_SIZE, TILE_SIZE)),
                ],
                "east": [
                    pygame.transform.scale(pygame.image.load(path + "Non-Educated-NPC/East 1.png"), (TILE_SIZE, TILE_SIZE)),
                    pygame.transform.scale(pygame.image.load(path + "Non-Educated-NPC/East 2.png"), (TILE_SIZE, TILE_SIZE)),
                ],
                "west": [
                    pygame.transform.scale(pygame.image.load(path + "Non-Educated-NPC/West 1.png"), (TILE_SIZE, TILE_SIZE)),
                    pygame.transform.scale(pygame.image.load(path + "Non-Educated-NPC/West 2.png"), (TILE_SIZE, TILE_SIZE)),
                ],
            }
        },
    }


def draw_map(screen):
    """
    Draws the tile map by blitting each tile image from _assets.
    """
    for y in range(ROWS):
        for x in range(COLS):
            tile_type = tile_map[y][x]
            img = _assets.get(tile_type)
            if img:
                screen.blit(img, (x * TILE_SIZE, y * TILE_SIZE))


def draw_entities(screen, player_bot):
    """
    Draws all entities (bins, trash, NPCs, and the player bot).
    """
    # Draw bins
    for b in bins:
        screen.blit(_assets.get("trash_bin"), (b.x * TILE_SIZE, b.y * TILE_SIZE))
    # Draw trash
    for t in trashes:
        screen.blit(t.image, (t.x * TILE_SIZE, t.y * TILE_SIZE))
    # Draw NPCs
    for npc in npcs:
        screen.blit(npc.image, (npc.pixel_x, npc.pixel_y))
    # Draw player bot
    screen.blit(player_bot.image, (player_bot.pixel_x, player_bot.pixel_y))


def draw_menu(screen, npc_list):
    """
    Draws the NPC menu with details and upgrade buttons.
    """
    # Draw a semi-transparent gray overlay on the background
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((50, 50, 50, 150))  # RGBA: Dark gray with 150 alpha (transparency)
    screen.blit(overlay, (0, 0))

    # Draw the menu background
    menu_width, menu_height = screen.get_width() - 200, screen.get_height() - 200
    menu_bg_rect = pygame.Rect(100, 100, menu_width, menu_height)
    pygame.draw.rect(screen, (50, 50, 50), menu_bg_rect)  # Dark gray background
    pygame.draw.rect(screen, (255, 255, 255), menu_bg_rect, 2)  # White border

    font = pygame.font.SysFont(None, 24)

    # Draw the title
    title_text = font.render("NPC Menu", True, (255, 255, 255))  # White text
    screen.blit(title_text, (menu_bg_rect.x + menu_width // 2 - 50, menu_bg_rect.y + 20))  # Centered title

    # Draw NPC details and images
    y_offset = menu_bg_rect.y + 60
    for npc in npc_list:
        # Draw NPC image
        npc_image = _assets["npc"][npc["type"]]["walk"]["south"][0]  # Use the south-facing image
        screen.blit(npc_image, (menu_bg_rect.x + 20, y_offset))  # Display image on the left

        # Draw NPC details
        npc_text = f"{npc['name']} (Lv. {npc['level']}) - {npc['location']}"
        npc_surface = font.render(npc_text, True, (255, 255, 255))  # White text
        screen.blit(npc_surface, (menu_bg_rect.x + 100, y_offset + 10))  # Display text next to the image

        # Draw upgrade button
        upgrade_button_rect = pygame.Rect(menu_bg_rect.x + menu_width - 170, y_offset, 150, 40)
        pygame.draw.rect(screen, (100, 200, 100), upgrade_button_rect)  # Green button
        upgrade_text = font.render("Upgrade", True, (0, 0, 0))  # Black text
        screen.blit(upgrade_text, (upgrade_button_rect.x + 20, upgrade_button_rect.y + 10))

        # Update the button rect in the NPC dictionary
        npc["upgrade_button"] = upgrade_button_rect
        y_offset += 80  # Move to the next NPC


def display_stats(screen, money, bot_capacity, bot_current_trash):
    """
    Displays the player's stats (money, bot capacity, etc.).
    """
    font = pygame.font.SysFont(None, 36)  # Font size 36
    # Display money
    money_text = f"Money: ${money}"
    money_surface = font.render(money_text, True, (0, 0, 0))  # Black text
    screen.blit(money_surface, (10, 10))  # Top-left corner

    # Display bot capacity
    capacity_text = f"Bot Capacity: {bot_current_trash}/{bot_capacity}"
    capacity_surface = font.render(capacity_text, True, (0, 0, 0))  # Black text
    screen.blit(capacity_surface, (10, 50))  # Below the money text

    # Display upgrade instructions at the bottom-left corner
    upgrade_text = f"[1] (${capacity_upgrade_cost}) to upgrade capacity"
    upgrade_surface = font.render(upgrade_text, True, (0, 0, 0))  # Black text
    screen.blit(upgrade_surface, (10, screen.get_height() - 50))  # Bottom-left corner

    upgrade_text = f"[2] (${speed_upgrade_cost}) to upgrade speed"
    upgrade_surface = font.render(upgrade_text, True, (0, 0, 0))  # Black text
    screen.blit(upgrade_surface, (10, screen.get_height() - 25))  # Bottom-left corner
