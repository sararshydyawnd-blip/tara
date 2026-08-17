import tkinter as tk
import random
import math

WIDTH = 900
HEIGHT = 650

PLAYER_SPEED = 8
BULLET_SPEED = 12
ENEMY_SPEED = 3


class SpaceBattle:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 SPACE BATTLE")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            bg="#05051a",
            highlightthickness=0
        )
        self.canvas.pack()

        self.keys = set()

        self.score = 0
        self.health = 100
        self.level = 1
        self.game_over = False

        self.bullets = []
        self.enemies = []
        self.stars = []

        self.player_x = WIDTH // 2
        self.player_y = HEIGHT - 80

        self.enemy_timer = 0
        self.shoot_cooldown = 0

        self.create_stars()
        self.create_player()

        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)

        self.game_loop()

    # -------------------------------------------------
    # BACKGROUND
    # -------------------------------------------------

    def create_stars(self):
        for _ in range(120):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            speed = random.randint(1, 4)

            star = self.canvas.create_oval(
                x,
                y,
                x + 2,
                y + 2,
                fill="white",
                outline=""
            )

            self.stars.append(
                [star, speed]
            )

    def update_stars(self):
        for star, speed in self.stars:
            self.canvas.move(
                star,
                0,
                speed
            )

            coords = self.canvas.coords(star)

            if coords[1] > HEIGHT:
                self.canvas.move(
                    star,
                    0,
                    -HEIGHT
                )

    # -------------------------------------------------
    # PLAYER
    # -------------------------------------------------

    def create_player(self):
        self.player = self.canvas.create_polygon(
            self.player_x,
            self.player_y - 30,

            self.player_x - 25,
            self.player_y + 25,

            self.player_x,
            self.player_y + 15,

            self.player_x + 25,
            self.player_y + 25,

            fill="#00eaff",
            outline="#ffffff",
            width=2
        )

        self.engine = self.canvas.create_polygon(
            self.player_x - 10,
            self.player_y + 20,

            self.player_x,
            self.player_y + 45,

            self.player_x + 10,
            self.player_y + 20,

            fill="#ff5500",
            outline=""
        )

    def move_player(self):
        dx = 0
        dy = 0

        if "Left" in self.keys or "a" in self.keys:
            dx -= PLAYER_SPEED

        if "Right" in self.keys or "d" in self.keys:
            dx += PLAYER_SPEED

        if "Up" in self.keys or "w" in self.keys:
            dy -= PLAYER_SPEED

        if "Down" in self.keys or "s" in self.keys:
            dy += PLAYER_SPEED

        self.canvas.move(
            self.player,
            dx,
            dy
        )

        self.canvas.move(
            self.engine,
            dx,
            dy
        )

        coords = self.canvas.coords(
            self.player
        )

        if coords:
            xs = coords[::2]
            ys = coords[1::2]

            min_x = min(xs)
            max_x = max(xs)
            min_y = min(ys)
            max_y = max(ys)

            if min_x < 0:
                self.canvas.move(
                    self.player,
                    -min_x,
                    0
                )
                self.canvas.move(
                    self.engine,
                    -min_x,
                    0
                )

            if max_x > WIDTH:
                self.canvas.move(
                    self.player,
                    WIDTH - max_x,
                    0
                )
                self.canvas.move(
                    self.engine,
                    WIDTH - max_x,
                    0
                )

            if min_y < HEIGHT // 2:
                self.canvas.move(
                    self.player,
                    0,
                    HEIGHT // 2 - min_y
                )
                self.canvas.move(
                    self.engine,
                    0,
                    HEIGHT // 2 - min_y
                )

            if max_y > HEIGHT - 20:
                self.canvas.move(
                    self.player,
                    0,
                    HEIGHT - 20 - max_y
                )
                self.canvas.move(
                    self.engine,
                    0,
                    HEIGHT - 20 - max_y
                )

    # -------------------------------------------------
    # SHOOTING
    # -------------------------------------------------

    def shoot(self):
        if self.shoot_cooldown > 0:
            return

        coords = self.canvas.coords(
            self.player
        )

        x = sum(coords[::2]) / len(coords[::2])
        y = min(coords[1::2])

        bullet = self.canvas.create_rectangle(
            x - 3,
            y - 15,
            x + 3,
            y,
            fill="#00ffff",
            outline=""
        )

        self.bullets.append(
            bullet
        )

        self.shoot_cooldown = 8

    def update_bullets(self):
        for bullet in self.bullets[:]:

            self.canvas.move(
                bullet,
                0,
                -BULLET_SPEED
            )

            coords = self.canvas.coords(
                bullet
            )

            if not coords:
                self.bullets.remove(
                    bullet
                )
                continue

            if coords[3] < 0:
                self.canvas.delete(
                    bullet
                )

                self.bullets.remove(
                    bullet
                )

    # -------------------------------------------------
    # ENEMIES
    # -------------------------------------------------

    def spawn_enemy(self):
        x = random.randint(
            40,
            WIDTH - 40
        )

        enemy_type = random.choice(
            ["normal", "fast", "tank"]
        )

        if enemy_type == "normal":
            size = 20
            hp = 1
            speed = ENEMY_SPEED

            color = "#ff3355"

        elif enemy_type == "fast":
            size = 14
            hp = 1
            speed = ENEMY_SPEED + 3

            color = "#ffaa00"

        else:
            size = 30
            hp = 3
            speed = ENEMY_SPEED - 1

            color = "#aa33ff"

        enemy = self.canvas.create_oval(
            x - size,
            -size,
            x + size,
            size,
            fill=color,
            outline="#ffffff",
            width=1
        )

        self.enemies.append(
            {
                "id": enemy,
                "hp": hp,
                "speed": speed,
                "type": enemy_type
            }
        )

    def update_enemies(self):
        for enemy in self.enemies[:]:

            obj = enemy["id"]

            self.canvas.move(
                obj,
                0,
                enemy["speed"]
            )

            coords = self.canvas.coords(
                obj
            )

            if not coords:
                self.enemies.remove(
                    enemy
                )
                continue

            if coords[1] > HEIGHT:

                self.canvas.delete(
                    obj
                )

                self.enemies.remove(
                    enemy
                )

                self.damage_player(
                    10
                )

    # -------------------------------------------------
    # COLLISION
    # -------------------------------------------------

    def collision(self, a, b):

        box_a = self.canvas.bbox(a)
        box_b = self.canvas.bbox(b)

        if not box_a or not box_b:
            return False

        return not (
            box_a[2] < box_b[0]
            or
            box_a[0] > box_b[2]
            or
            box_a[3] < box_b[1]
            or
            box_a[1] > box_b[3]
        )

    def check_collisions(self):

        for bullet in self.bullets[:]:

            for enemy in self.enemies[:]:

                if self.collision(
                    bullet,
                    enemy["id"]
                ):

                    self.canvas.delete(
                        bullet
                    )

                    if bullet in self.bullets:
                        self.bullets.remove(
                            bullet
                        )

                    enemy["hp"] -= 1

                    if enemy["hp"] <= 0:

                        self.destroy_enemy(
                            enemy
                        )

                    break

        for enemy in self.enemies[:]:

            if self.collision(
                self.player,
                enemy["id"]
            ):

                self.destroy_enemy(
                    enemy
                )

                self.damage_player(
                    20
                )

    def destroy_enemy(self, enemy):

        obj = enemy["id"]

        self.canvas.delete(
            obj
        )

        if enemy in self.enemies:
            self.enemies.remove(
                enemy
            )

        if enemy["type"] == "tank":
            self.score += 30

        elif enemy["type"] == "fast":
            self.score += 20

        else:
            self.score += 10

        self.update_hud()

        if self.score % 200 == 0:
            self.level += 1

    # -------------------------------------------------
    # PLAYER DAMAGE
    # -------------------------------------------------

    def damage_player(self, amount):

        self.health -= amount

        if self.health <= 0:
            self.health = 0
            self.end_game()

        self.update_hud()

    # -------------------------------------------------
    # HUD
    # -------------------------------------------------

    def create_hud(self):

        self.hud = self.canvas.create_text(
            20,
            20,
            anchor="nw",
            text="",
            fill="white",
            font=("Arial", 16, "bold")
        )

        self.update_hud()

    def update_hud(self):

        if not hasattr(self, "hud"):
            self.create_hud()
            return

        text = (
            f"SCORE: {self.score}     "
            f"HP: {self.health}     "
            f"LEVEL: {self.level}"
        )

        self.canvas.itemconfig(
            self.hud,
            text=text
        )

    # -------------------------------------------------
    # GAME LOOP
    # -------------------------------------------------

    def game_loop(self):

        if self.game_over:
            return

        self.update_stars()
        self.move_player()
        self.update_bullets()
        self.update_enemies()
        self.check_collisions()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if (
            "space" in self.keys
            or "Space" in self.keys
        ):
            self.shoot()

        self.enemy_timer += 1

        spawn_rate = max(
            15,
            50 - self.level * 3
        )

        if self.enemy_timer >= spawn_rate:

            self.spawn_enemy()

            self.enemy_timer = 0

        self.root.after(
            16,
            self.game_loop
        )

    # -------------------------------------------------
    # INPUT
    # -------------------------------------------------

    def key_down(self, event):

        self.keys.add(
            event.keysym
        )

        if event.keysym.lower() == "r":
            if self.game_over:
                self.restart()

    def key_up(self, event):

        self.keys.discard(
            event.keysym
        )

    # -------------------------------------------------
    # GAME OVER
    # -------------------------------------------------

    def end_game(self):

        self.game_over = True

        self.canvas.create_rectangle(
            0,
            0,
            WIDTH,
            HEIGHT,
            fill="#000000",
            stipple="gray50",
            outline=""
        )

        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 - 50,
            text="GAME OVER",
            fill="#ff3355",
            font=(
                "Arial",
                48,
                "bold"
            )
        )

        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 20,
            text=f"Score: {self.score}",
            fill="white",
            font=(
                "Arial",
                24,
                "bold"
            )
        )

        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 70,
            text="Press R to restart",
            fill="#00ffff",
            font=(
                "Arial",
                18
            )
        )

    # -------------------------------------------------
    # RESTART
    # -------------------------------------------------

    def restart(self):

        self.canvas.delete(
            "all"
        )

        self.keys.clear()

        self.score = 0
        self.health = 100
        self.level = 1

        self.bullets.clear()
        self.enemies.clear()
        self.stars.clear()

        self.game_over = False
        self.enemy_timer = 0
        self.shoot_cooldown = 0

        self.create_stars()
        self.create_player()

        self.create_hud()

        self.game_loop()


def main():

    root = tk.Tk()

    game = SpaceBattle(
        root
    )

    game.create_hud()

    root.mainloop()


if __name__ == "__main__":
    main()