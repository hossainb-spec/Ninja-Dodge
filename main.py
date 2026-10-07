import random
import pygame


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ninja Dodge by Barack, Aiden, Sha, and Rehan")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 72)
ARENA = pygame.Rect(40, 70, 720, 490)




def draw_ninja(position, color, direction, radius, show_head=True):
    scale = radius / 9
    sprite = pygame.Surface((round(20 * scale), round(25 * scale)), pygame.SRCALPHA)
    red_team = color[0] > color[2]
    outline = (8, 22, 34)
    shadow = (12, 38, 52) if not red_team else (48, 22, 33)
    cloth = (24, 70, 82) if not red_team else (105, 43, 52)
    highlight = (39, 100, 108) if not red_team else (145, 61, 65)
    skin = (232, 164, 107)
    belt = (13, 48, 66) if not red_team else (66, 30, 42)


    def block(x, y, width, height, fill):
        rect = pygame.Rect(round(x * scale), round(y * scale), max(1, round(width * scale)), max(1, round(height * scale)))
        pygame.draw.rect(sprite, fill, rect)


    if show_head:
        block(5, 0, 10, 7, outline)
        block(4, 1, 12, 5, outline)
        block(6, 1, 8, 4, shadow)
        block(7, 4, 8, 4, skin)
        block(8, 6, 2, 1, outline)
        block(13, 6, 2, 1, outline)
        block(6, 7, 11, 2, shadow)
        block(4, 2, 2, 4, shadow)
        block(14, 2, 2, 4, shadow)
        block(7, 1, 7, 1, highlight)


    block(4, 8, 12, 8, outline)
    block(1, 9, 5, 4, outline)
    block(14, 9, 5, 4, outline)
    block(2, 10, 4, 2, cloth)
    block(14, 10, 4, 2, cloth)
    block(18, 10, 2, 2, skin)
    block(5, 9, 10, 6, cloth)
    block(6, 9, 8, 2, highlight)
    block(8, 11, 2, 2, shadow)
    block(12, 11, 2, 2, shadow)
    block(5, 14, 10, 2, belt)
    block(9, 14, 2, 2, highlight)
    block(5, 16, 5, 7, outline)
    block(10, 16, 5, 7, outline)
    block(6, 16, 3, 6, cloth)
    block(11, 16, 3, 6, cloth)
    block(6, 18, 3, 1, highlight)
    block(11, 18, 3, 1, highlight)
    block(3, 22, 6, 3, outline)
    block(11, 22, 6, 3, outline)
    block(4, 22, 4, 1, shadow)
    block(12, 22, 4, 1, shadow)
    flipped = pygame.transform.flip(sprite, direction.x < 0, False)
    center = (round(position.x), round(position.y - 0.5 * scale))
    screen.blit(flipped, flipped.get_rect(center=center))




def draw_player_sprite(position, show_head=True):
    scale = 16 / 9
    origin_x = round(position.x - 12 * scale)
    origin_y = round(position.y - 15 * scale)


    def block(x, y, width, height, color):
        rect = pygame.Rect(origin_x + round(x * scale), origin_y + round(y * scale), max(1, round(width * scale)), max(1, round(height * scale)))
        pygame.draw.rect(screen, color, rect)


    outline = (20, 25, 35)
    hair = (28, 27, 34)
    skin = (205, 150, 119)
    shirt = (67, 133, 194)
    stripe = (37, 72, 119)
    pants = (35, 42, 55)
    shoes = (18, 23, 32)


    if show_head:
        block(6, 1, 11, 8, outline)
        block(7, 0, 9, 3, hair)
        block(5, 2, 2, 5, hair)
        block(16, 2, 2, 5, hair)
        block(7, 3, 9, 6, skin)
        block(8, 6, 2, 1, outline)
        block(13, 6, 2, 1, outline)
        block(8, 8, 7, 1, (135, 88, 77))
        block(9, 9, 5, 2, skin)


    block(4, 10, 16, 11, outline)
    block(2, 11, 5, 8, outline)
    block(17, 11, 5, 8, outline)
    block(3, 12, 3, 6, shirt)
    block(18, 12, 3, 6, shirt)
    block(5, 11, 14, 9, shirt)
    for y in (13, 16, 19):
        block(3, y, 3, 1, stripe)
        block(18, y, 3, 1, stripe)
        block(5, y, 14, 1, stripe)
    block(5, 20, 7, 7, outline)
    block(12, 20, 7, 7, outline)
    block(6, 20, 5, 6, pants)
    block(13, 20, 5, 6, pants)
    block(4, 26, 7, 3, shoes)
    block(13, 26, 7, 3, shoes)




class Player:
    def __init__(self):
        self.position = pygame.Vector2(400, 300)
        self.facing = pygame.Vector2(0, -1)
        self.health = 3
        self.invincible = 0
        self.speed_multiplier = 1.0
        self.powerup_timer = 0
        self.powerup_amount = 0


    def power_up(self, level):
        self.powerup_amount = max(0.001, 0.01 - (level - 1) * 0.001)
        self.speed_multiplier += self.powerup_amount
        self.powerup_timer = 1.4


    def update(self, dt):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])
        if direction.length() > 0:
            direction = direction.normalize()
            self.facing = direction
        self.position += direction * 240 * self.speed_multiplier * dt
        self.position.x = max(54, min(746, self.position.x))
        self.position.y = max(84, min(546, self.position.y))
        self.invincible = max(0, self.invincible - dt)
        self.powerup_timer = max(0, self.powerup_timer - dt)


    def draw(self):
        if self.invincible <= 0 or int(self.invincible * 10) % 2 == 0:
            draw_ninja(self.position, (65, 95, 130), self.facing, 18)
        if self.powerup_timer > 0:
            label = font.render(f"POWER UP +{self.powerup_amount * 100:.1f}%", True, (150, 235, 175))
            screen.blit(label, label.get_rect(center=(self.position.x, self.position.y - 43)))




class Enemy:
    def __init__(self):
        self.position = pygame.Vector2(random.randint(70, 730), random.randint(100, 530))
        self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()
        self.timer = random.uniform(1, 3)
        self.alert = 0
        self.target = self.position.copy()


    def update(self, dt, player, lasers):
        if self.alert > 0:
            direction_to_player = player.position - self.position
            if direction_to_player.length() > 250:
                self.alert = 0
                return
            self.target = player.position.copy()
            if direction_to_player.length() > 0:
                self.direction = direction_to_player.normalize()
            self.alert -= dt
            if self.alert <= 0:
                laser_direction = player.position - self.position
                if laser_direction.length() > 0:
                    lasers.append([self.position.copy(), laser_direction.normalize() * 430])
                self.timer = 1.5
            return


        self.position += self.direction * 65 * dt
        if self.position.x < 56 or self.position.x > 744:
            self.direction.x *= -1
        if self.position.y < 86 or self.position.y > 544:
            self.direction.y *= -1
        self.position.x = max(56, min(744, self.position.x))
        self.position.y = max(86, min(544, self.position.y))
        distance = self.position.distance_to(player.position)
        if distance < 250:
            direction_to_player = (player.position - self.position).normalize()
            if self.direction.dot(direction_to_player) > 0:
                self.alert = 1.5
                self.target = player.position.copy()
        self.timer -= dt
        if self.timer <= 0:
            self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            self.timer = random.uniform(1, 3)


    def draw(self):
        color = (165, 75, 80) if self.alert > 0 else (135, 55, 65)
        draw_ninja(self.position, color, self.direction, 18)
        pygame.draw.line(screen, (255, 210, 210), self.position, self.position + self.direction * 24, 3)
        if self.alert > 0:
            pygame.draw.line(screen, (255, 70, 70), self.position, self.target, 2)




def new_game():
    return Player(), [Enemy(), Enemy()], [], 0, 7




player, enemies, lasers, elapsed, spawn_timer = new_game()
running = True


while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and player.health <= 0:
            player, enemies, lasers, elapsed, spawn_timer = new_game()


    if player.health > 0:
        previous_elapsed = elapsed
        elapsed += dt
        if int(elapsed) // 10 > int(previous_elapsed) // 10:
            player.power_up(int(elapsed) // 10)
        player.update(dt)
        spawn_timer -= dt
        if spawn_timer <= 0:
            enemies.append(Enemy())
            spawn_timer = max(2.5, 7 - elapsed / 15)
        for enemy in enemies:
            enemy.update(dt, player, lasers)
        for laser in lasers[:]:
            laser[0] += laser[1] * dt
            if not ARENA.collidepoint(laser[0]):
                lasers.remove(laser)
            elif player.invincible <= 0 and laser[0].distance_to(player.position) < 20:
                player.health -= 1
                player.invincible = 1
                lasers.remove(laser)


    screen.fill((0, 0, 0))
    score = int(elapsed * 750)
    if player.health > 0:
        screen.fill((20, 24, 40))
        pygame.draw.rect(screen, (100, 110, 140), ARENA, 2)
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for position, velocity in lasers:
            end = position + velocity.normalize() * 18
            pygame.draw.line(screen, (255, 55, 65), position, end, 4)
            pygame.draw.circle(screen, (255, 220, 220), end, 4)
        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (50, 18))
        screen.blit(font.render(f"Health: {player.health}", True, (255, 255, 255)), (210, 18))
        screen.blit(font.render("WASD to move", True, (200, 205, 220)), (620, 18))
    else:
        screen.blit(big_font.render("YOU LOST", True, (230, 55, 65)), (300, 225))
        screen.blit(font.render(f"FINAL SCORE: {score}", True, (225, 205, 205)), (320, 310))
        screen.blit(font.render("Press R to try again  |  Esc to quit", True, (205, 185, 190)), (255, 370))


    pygame.display.flip()


pygame.quit()





