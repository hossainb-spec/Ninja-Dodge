import random
import pygame
import asyncio

WIDTH, HEIGHT = 800, 600

ARENA = pygame.Rect(40, 70, 720, 490)


class Player:
    def __init__(self):
        self.position = pygame.Vector2(400, 300)
        self.health = 3
        self.invincible = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()

        direction = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w]
        )

        if direction.length() > 0:
            direction = direction.normalize()

        self.position += direction * 240 * dt

        self.position.x = max(54, min(746, self.position.x))
        self.position.y = max(84, min(546, self.position.y))

        if self.invincible > 0:
            self.invincible -= dt

    def draw(self):
        if self.invincible <= 0 or int(self.invincible * 10) % 2 == 0:
            pygame.draw.circle(screen, (245, 245, 255), self.position, 14)
            pygame.draw.circle(
                screen,
                (100, 200, 255),
                self.position,
                14,
                2
            )


class Enemy:
    def __init__(self):
        self.position = pygame.Vector2(
            random.randint(70, 730),
            random.randint(100, 530)
        )

        self.direction = pygame.Vector2(
            random.choice([-1, 1]),
            random.choice([-1, 1])
        ).normalize()

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
                    laser_direction = laser_direction.normalize()

                    lasers.append([
                        self.position.copy(),
                        laser_direction * 430
                    ])

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
            direction_to_player = player.position - self.position

            if direction_to_player.length() > 0:
                direction_to_player = direction_to_player.normalize()

                if self.direction.dot(direction_to_player) > 0:
                    self.alert = 1.5
                    self.target = player.position.copy()

        self.timer -= dt

        if self.timer <= 0:
            new_direction = pygame.Vector2(
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            )

            if new_direction.length() > 0:
                self.direction = new_direction.normalize()

            self.timer = random.uniform(1, 3)

    def draw(self):
        if self.alert > 0:
            color = (255, 100, 100)
        else:
            color = (220, 55, 75)

        pygame.draw.circle(
            screen,
            color,
            self.position,
            16
        )

        pygame.draw.line(
            screen,
            (255, 210, 210),
            self.position,
            self.position + self.direction * 24,
            3
        )

        if self.alert > 0:
            pygame.draw.line(
                screen,
                (255, 70, 70),
                self.position,
                self.target,
                2
            )


def new_game():
    player = Player()
    enemies = [Enemy(), Enemy()]
    lasers = []

    return player, enemies, lasers, 0, 7


async def main():
    global screen

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ninja Dodge")

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 32)
    big_font = pygame.font.Font(None, 72)

    player, enemies, lasers, elapsed, spawn_timer = new_game()

    running = True

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_r and player.health <= 0:
                    player, enemies, lasers, elapsed, spawn_timer = new_game()

        if player.health > 0:
            elapsed += dt
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

                elif player.invincible <= 0:
                    if laser[0].distance_to(player.position) < 20:
                        player.health -= 1
                        player.invincible = 1
                        lasers.remove(laser)

        screen.fill((20, 24, 40))

        pygame.draw.rect(
            screen,
            (100, 110, 140),
            ARENA,
            2
        )

        player.draw()

        for enemy in enemies:
            enemy.draw()

        for position, velocity in lasers:
            end = position + velocity.normalize() * 18

            pygame.draw.line(
                screen,
                (255, 55, 65),
                position,
                end,
                4
            )

            pygame.draw.circle(
                screen,
                (255, 220, 220),
                end,
                4
            )

        score = int(elapsed * 1000)

        screen.blit(
            font.render(
                f"Score: {score}",
                True,
                (255, 255, 255)
            ),
            (50, 18)
        )

        screen.blit(
            font.render(
                f"Health: {player.health}",
                True,
                (255, 255, 255)
            ),
            (210, 18)
        )

        screen.blit(
            font.render(
                "WASD to move",
                True,
                (200, 205, 220)
            ),
            (620, 18)
        )

        if player.health <= 0:
            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            screen.blit(
                big_font.render(
                    "GAME OVER",
                    True,
                    (255, 255, 255)
                ),
                (275, 210)
            )

            screen.blit(
                font.render(
                    f"Final score: {score}",
                    True,
                    (255, 255, 255)
                ),
                (335, 290)
            )

            screen.blit(
                font.render(
                    "Press R to play again | Esc to quit",
                    True,
                    (220, 220, 230)
                ),
                (260, 335)
            )

        pygame.display.flip()

        # Process Bling Bling:
        # Give the browser control so the web game does not freeze.
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
