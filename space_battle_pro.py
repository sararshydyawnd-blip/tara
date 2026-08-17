import tkinter as tk
import random
import math
import json
import os

# ============================================================
# SPACE BATTLE PRO
# A Python/Tkinter arcade shooter
# ============================================================

WIDTH = 1000
HEIGHT = 700
FPS = 16

SAVE_FILE = "space_battle_highscore.json"


class Particle:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.x = x
        self.y = y

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 7)

        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

        self.life = random.randint(15, 35)

        size = random.randint(2, 5)

        self.id = canvas.create_oval(
            x - size,
            y - size,
            x + size,
            y + size,
            fill=color,
            outline=""
        )

    def update(self):

        self.x += self.dx
        self.y += self.dy

        self.dy += 0.08

        self.life -= 1

        self.canvas.move(
            self.id,
            self.dx,
            self.dy
        )

        if self.life <= 0:
            self.canvas.delete(self.id)
            return False

        return True


class SpaceBattlePro:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "🚀 SPACE BATTLE PRO"
        )

        self.root.resizable(
            False,
            False
        )

        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            bg="#02030f",
            highlightthickness=0
        )

        self.canvas.pack()

        # ----------------------------------------------------
        # INPUT
        # ----------------------------------------------------

        self.keys = set()

        self.root.bind(
            "<KeyPress>",
            self.key_down
        )

        self.root.bind(
            "<KeyRelease>",
            self.key_up
        )

        # ----------------------------------------------------
        # GAME DATA
        # ----------------------------------------------------

        self.score = 0

        self.high_score = self.load_high_score()

        self.level = 1

        self.xp = 0

        self.next_level_xp = 500

        self.player_hp = 100

        self.player_max_hp = 100

        self.shield = 100

        self.max_shield = 100

        self.weapon_level = 1

        self.special_energy = 0

        self.game_over = False

        self.paused = False

        self.boss = None

        self.boss_active = False

        # ----------------------------------------------------
        # OBJECTS
        # ----------------------------------------------------

        self.stars = []

        self.bullets = []

        self.enemies = []

        self.enemy_bullets = []

        self.powerups = []

        self.particles = []

        self.explosions = []

        # ----------------------------------------------------
        # PLAYER
        # ----------------------------------------------------

        self.player_x = WIDTH // 2

        self.player_y = HEIGHT - 100

        self.player_speed = 8

        self.shoot_cooldown = 0

        self.special_cooldown = 0

        # ----------------------------------------------------
        # TIMERS
        # ----------------------------------------------------

        self.enemy_timer = 0

        self.powerup_timer = 0

        self.boss_timer = 0

        # ----------------------------------------------------
        # MENU
        # ----------------------------------------------------

        self.show_start_screen()

    # ========================================================
    # HIGH SCORE
    # ========================================================

    def load_high_score(self):

        try:

            if os.path.exists(
                SAVE_FILE
            ):

                with open(
                    SAVE_FILE,
                    "r"
                ) as f:

                    data = json.load(f)

                    return int(
                        data.get(
                            "high_score",
                            0
                        )
                    )

        except Exception:
            pass

        return 0

    def save_high_score(self):

        try:

            with open(
                SAVE_FILE,
                "w"
            ) as f:

                json.dump(
                    {
                        "high_score":
                        self.high_score
                    },
                    f
                )

        except Exception:
            pass

    # ========================================================
    # START SCREEN
    # ========================================================

    def show_start_screen(self):

        self.canvas.delete(
            "all"
        )

        self.canvas.create_text(
            WIDTH // 2,
            160,
            text="SPACE BATTLE",
            fill="#00eaff",
            font=(
                "Arial",
                58,
                "bold"
            )
        )

        self.canvas.create_text(
            WIDTH // 2,
            225,
            text="PRO",
            fill="#ff3355",
            font=(
                "Arial",
                45,
                "bold"
            )
        )

        self.canvas.create_text(
            WIDTH // 2,
            330,
            text="PRESS ENTER TO START",
            fill="white",
            font=(
                "Arial",
                22,
                "bold"
            )
        )

        self.canvas.create_text(
            WIDTH // 2,
            390,
            text="WASD / ARROWS = MOVE",
            fill="#aaaaaa",
            font=(
                "Arial",
                15
            )
        )

        self.canvas.create_text(
            WIDTH // 2,
            420,
            text="SPACE = SHOOT",
            fill="#aaaaaa",
            font=(
                "Arial",
                15
            )
        )

        self.canvas.create_text(
            WIDTH // 2,
            450,
            text="E = SPECIAL WEAPON",
            fill="#aaaaaa",
            font=(
                "Arial",
                15
            )
        )

        self.canvas.create_text(
            WIDTH // 2,
            500,
            text=f"HIGH SCORE: {self.high_score}",
            fill="#ffd700",
            font=(
                "Arial",
                18,
                "bold"
            )
        )

        self.in_menu = True

    # ========================================================
    # START GAME
    # ========================================================

    def start_game(self):

        self.canvas.delete(
            "all"
        )

        self.in_menu = False

        self.score = 0

        self.level = 1

        self.xp = 0

        self.next_level_xp = 500

        self.player_hp = 100

        self.shield = 100

        self.weapon_level = 1

        self.special_energy = 0

        self.game_over = False

        self.paused = False

        self.boss = None

        self.boss_active = False

        self.stars.clear()

        self.bullets.clear()

        self.enemies.clear()

        self.enemy_bullets.clear()

        self.powerups.clear()

        self.particles.clear()

        self.create_stars()

        self.create_player()

        self.create_hud()

        self.game_loop()

    # ========================================================
    # STARS
    # ========================================================

    def create_stars(self):

        for _ in range(160):

            x = random.randint(
                0,
                WIDTH
            )

            y = random.randint(
                0,
                HEIGHT
            )

            speed = random.randint(
                1,
                5
            )

            size = random.choice(
                [1, 1, 2, 2, 3]
            )

            star = self.canvas.create_oval(
                x,
                y,
                x + size,
                y + size,
                fill="white",
                outline=""
            )

            self.stars.append(
                [
                    star,
                    speed
                ]
            )

    def update_stars(self):

        for star, speed in self.stars:

            self.canvas.move(
                star,
                0,
                speed
            )

            coords = self.canvas.coords(
                star
            )

            if coords and coords[1] > HEIGHT:

                self.canvas.move(
                    star,
                    0,
                    -HEIGHT
                )

    # ========================================================
    # PLAYER
    # ========================================================

    def create_player(self):

        x = self.player_x
        y = self.player_y

        self.player = self.canvas.create_polygon(

            x,
            y - 40,

            x - 35,
            y + 35,

            x,
            y + 20,

            x + 35,
            y + 35,

            fill="#00eaff",

            outline="#ffffff",

            width=2
        )

        self.engine = self.canvas.create_polygon(

            x - 12,
            y + 20,

            x,
            y + 55,

            x + 12,
            y + 20,

            fill="#ff6600",

            outline=""
        )

        self.shield_graphic = None

    def update_player(self):

        dx = 0
        dy = 0

        if (
            "Left" in self.keys
            or "a" in self.keys
        ):
            dx -= self.player_speed

        if (
            "Right" in self.keys
            or "d" in self.keys
        ):
            dx += self.player_speed

        if (
            "Up" in self.keys
            or "w" in self.keys
        ):
            dy -= self.player_speed

        if (
            "Down" in self.keys
            or "s" in self.keys
        ):
            dy += self.player_speed

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

        box = self.canvas.bbox(
            self.player
        )

        if not box:
            return

        left, top, right, bottom = box

        if left < 10:

            move = 10 - left

            self.canvas.move(
                self.player,
                move,
                0
            )

            self.canvas.move(
                self.engine,
                move,
                0
            )

        if right > WIDTH - 10:

            move = WIDTH - 10 - right

            self.canvas.move(
                self.player,
                move,
                0
            )

            self.canvas.move(
                self.engine,
                move,
                0
            )

        if top < HEIGHT // 2:

            move = HEIGHT // 2 - top

            self.canvas.move(
                self.player,
                0,
                move
            )

            self.canvas.move(
                self.engine,
                0,
                move
            )

        if bottom > HEIGHT - 15:

            move = HEIGHT - 15 - bottom

            self.canvas.move(
                self.player,
                0,
                move
            )

            self.canvas.move(
                self.engine,
                0,
                move
            )

    # ========================================================
    # SHOOTING
    # ========================================================

    def shoot(self):

        if self.shoot_cooldown > 0:
            return

        coords = self.canvas.coords(
            self.player
        )

        if not coords:
            return

        x = sum(
            coords[::2]
        ) / len(
            coords[::2]
        )

        y = min(
            coords[1::2]
        )

        if self.weapon_level == 1:

            self.create_bullet(
                x,
                y,
                0,
                -12
            )

        elif self.weapon_level == 2:

            self.create_bullet(
                x - 10,
                y,
                -0.5,
                -12
            )

            self.create_bullet(
                x + 10,
                y,
                0.5,
                -12
            )

        else:

            self.create_bullet(
                x,
                y,
                0,
                -13
            )

            self.create_bullet(
                x - 15,
                y + 5,
                -1,
                -12
            )

            self.create_bullet(
                x + 15,
                y + 5,
                1,
                -12
            )

        self.shoot_cooldown = max(
            4,
            11 - self.weapon_level * 2
        )

    def create_bullet(
        self,
        x,
        y,
        dx,
        dy
    ):

        bullet = self.canvas.create_oval(
            x - 4,
            y - 12,
            x + 4,
            y + 12,
            fill="#00ffff",
            outline=""
        )

        self.bullets.append(
            {
                "id": bullet,
                "dx": dx,
                "dy": dy,
                "damage": 1 + self.weapon_level
            }
        )

    def update_bullets(self):

        for bullet in self.bullets[:]:

            obj = bullet["id"]

            self.canvas.move(
                obj,
                bullet["dx"],
                bullet["dy"]
            )

            box = self.canvas.bbox(
                obj
            )

            if (
                not box
                or box[3] < 0
            ):

                self.canvas.delete(
                    obj
                )

                self.bullets.remove(
                    bullet
                )

    # ========================================================
    # ENEMIES
    # ========================================================

    def spawn_enemy(self):

        x = random.randint(
            40,
            WIDTH - 40
        )

        choice = random.random()

        if choice < 0.55:

            enemy_type = "normal"

            hp = 2 + self.level // 3

            speed = 2.5 + self.level * 0.15

            size = 22

            color = "#ff3355"

        elif choice < 0.80:

            enemy_type = "fast"

            hp = 1 + self.level // 5

            speed = 4 + self.level * 0.2

            size = 15

            color = "#ffaa00"

        else:

            enemy_type = "tank"

            hp = 8 + self.level

            speed = 1.5

            size = 32

            color = "#aa44ff"

        enemy = self.canvas.create_oval(

            x - size,
            -size * 2,

            x + size,
            0,

            fill=color,

            outline="#ffffff",

            width=2
        )

        self.enemies.append(
            {
                "id": enemy,
                "hp": hp,
                "max_hp": hp,
                "speed": speed,
                "type": enemy_type,
                "shoot_timer": random.randint(
                    40,
                    120
                )
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

            enemy["shoot_timer"] -= 1

            if (
                enemy["shoot_timer"] <= 0
                and enemy["type"] != "fast"
            ):

                self.enemy_shoot(
                    enemy
                )

                enemy["shoot_timer"] = random.randint(
                    70,
                    140
                )

            box = self.canvas.bbox(
                obj
            )

            if not box:
                continue

            if box[1] > HEIGHT:

                self.canvas.delete(
                    obj
                )

                self.enemies.remove(
                    enemy
                )

                self.damage_player(
                    10
                )

    # ========================================================
    # ENEMY SHOOT
    # ========================================================

    def enemy_shoot(self, enemy):

        box = self.canvas.bbox(
            enemy["id"]
        )

        if not box:
            return

        x = (
            box[0] + box[2]
        ) / 2

        y = box[3]

        bullet = self.canvas.create_oval(
            x - 5,
            y,
            x + 5,
            y + 12,
            fill="#ff2244",
            outline=""
        )

        self.enemy_bullets.append(
            {
                "id": bullet,
                "speed": 5 + self.level * 0.1
            }
        )

    def update_enemy_bullets(self):

        for bullet in self.enemy_bullets[:]:

            obj = bullet["id"]

            self.canvas.move(
                obj,
                0,
                bullet["speed"]
            )

            box = self.canvas.bbox(
                obj
            )

            if not box:
                continue

            if box[1] > HEIGHT:

                self.canvas.delete(
                    obj
                )

                self.enemy_bullets.remove(
                    bullet
                )

    # ========================================================
    # COLLISION
    # ========================================================

    def collision(self, a, b):

        box_a = self.canvas.bbox(a)
        box_b = self.canvas.bbox(b)

        if not box_a or not box_b:
            return False

        return not (
            box_a[2] < box_b[0]
            or box_a[0] > box_b[2]
            or box_a[3] < box_b[1]
            or box_a[1] > box_b[3]
        )

    def check_collisions(self):

        # Player bullets -> enemies

        for bullet in self.bullets[:]:

            for enemy in self.enemies[:]:

                if self.collision(
                    bullet["id"],
                    enemy["id"]
                ):

                    self.canvas.delete(
                        bullet["id"]
                    )

                    if bullet in self.bullets:

                        self.bullets.remove(
                            bullet
                        )

                    enemy["hp"] -= (
                        bullet["damage"]
                    )

                    if enemy["hp"] <= 0:

                        self.kill_enemy(
                            enemy
                        )

                    break

        # Player bullets -> boss

        if self.boss_active and self.boss:

            for bullet in self.bullets[:]:

                if self.collision(
                    bullet["id"],
                    self.boss["id"]
                ):

                    self.canvas.delete(
                        bullet["id"]
                    )

                    if bullet in self.bullets:

                        self.bullets.remove(
                            bullet
                        )

                    self.boss["hp"] -= (
                        bullet["damage"]
                    )

                    if self.boss["hp"] <= 0:

                        self.kill_boss()

                    break

        # Enemies -> player

        for enemy in self.enemies[:]:

            if self.collision(
                self.player,
                enemy["id"]
            ):

                self.kill_enemy(
                    enemy,
                    give_score=False
                )

                self.damage_player(
                    20
                )

        # Enemy bullets -> player

        for bullet in self.enemy_bullets[:]:

            if self.collision(
                self.player,
                bullet["id"]
            ):

                self.canvas.delete(
                    bullet["id"]
                )

                self.enemy_bullets.remove(
                    bullet
                )

                self.damage_player(
                    12
                )

        # Boss -> player

        if self.boss_active and self.boss:

            if self.collision(
                self.player,
                self.boss["id"]
            ):

                self.damage_player(
                    30
                )

    # ========================================================
    # ENEMY DEATH
    # ========================================================

    def kill_enemy(
        self,
        enemy,
        give_score=True
    ):

        box = self.canvas.bbox(
            enemy["id"]
        )

        if box:

            x = (
                box[0] + box[2]
            ) / 2

            y = (
                box[1] + box[3]
            ) / 2

            self.create_explosion(
                x,
                y,
                "#ff3355"
            )

        self.canvas.delete(
            enemy["id"]
        )

        if enemy in self.enemies:

            self.enemies.remove(
                enemy
            )

        if give_score:

            points = {
                "normal": 20,
                "fast": 35,
                "tank": 75
            }

            self.add_score(
                points[
                    enemy["type"]
                ]
            )

            self.add_xp(
                points[
                    enemy["type"]
                ]
            )

            if random.random() < 0.10:

                self.spawn_powerup_at(
                    x,
                    y
                )

    # ========================================================
    # BOSS
    # ========================================================

    def spawn_boss(self):

        if self.boss_active:
            return

        self.boss_active = True

        x = WIDTH // 2

        boss_id = self.canvas.create_oval(

            x - 110,
            60,

            x + 110,
            250,

            fill="#7700aa",

            outline="#ff44ff",

            width=5
        )

        self.boss = {

            "id": boss_id,

            "hp": 150 + self.level * 40,

            "max_hp": 150 + self.level * 40,

            "dx": 4,

            "shoot_timer": 50
        }

        self.canvas.create_text(
            WIDTH // 2,
            40,
            text="⚠ BOSS INCOMING ⚠",
            fill="#ff3355",
            font=(
                "Arial",
                24,
                "bold"
            ),
            tag="boss_warning"
        )

    def update_boss(self):

        if not self.boss_active:
            return

        if not self.boss:
            return

        boss = self.boss

        self.canvas.move(
            boss["id"],
            boss["dx"],
            0
        )

        box = self.canvas.bbox(
            boss["id"]
        )

        if box:

            if box[0] <= 20:

                boss["dx"] = abs(
                    boss["dx"]
                )

            if box[2] >= WIDTH - 20:

                boss["dx"] = -abs(
                    boss["dx"]
                )

        boss["shoot_timer"] -= 1

        if boss["shoot_timer"] <= 0:

            self.boss_shoot()

            boss["shoot_timer"] = 45

    def boss_shoot(self):

        if not self.boss:
            return

        box = self.canvas.bbox(
            self.boss["id"]
        )

        if not box:
            return

        x = (
            box[0] + box[2]
        ) / 2

        y = box[3]

        for dx in [-3, -1.5, 0, 1.5, 3]:

            bullet = self.canvas.create_oval(

                x - 7,
                y,

                x + 7,
                y + 14,

                fill="#ff00ff",

                outline=""
            )

            self.enemy_bullets.append(
                {
                    "id": bullet,
                    "speed": 6
                }
            )

    def kill_boss(self):

        if not self.boss:
            return

        box = self.canvas.bbox(
            self.boss["id"]
        )

        if box:

            x = (
                box[0] + box[2]
            ) / 2

            y = (
                box[1] + box[3]
            ) / 2

            for _ in range(40):

                self.create_particle(
                    x,
                    y,
                    random.choice(
                        [
                            "#ff00ff",
                            "#00ffff",
                            "#ffff00"
                        ]
                    )
                )

        self.canvas.delete(
            self.boss["id"]
        )

        self.boss = None

        self.boss_active = False

        self.add_score(
            1000
        )

        self.add_xp(
            1000
        )

        self.weapon_level = min(
            3,
            self.weapon_level + 1
        )

        self.canvas.delete(
            "boss_warning"
        )

    # ========================================================
    # POWER UPS
    # ========================================================

    def spawn_powerup_at(
        self,
        x,
        y
    ):

        types = [
            "health",
            "shield",
            "weapon",
            "energy"
        ]

        power_type = random.choice(
            types
        )

        colors = {
            "health": "#ff3355",
            "shield": "#00aaff",
            "weapon": "#ffaa00",
            "energy": "#aa00ff"
        }

        symbols = {
            "health": "+",
            "shield": "S",
            "weapon": "W",
            "energy": "E"
        }

        obj = self.canvas.create_oval(

            x - 14,
            y - 14,
            x + 14,
            y + 14,

            fill=colors[
                power_type
            ],

            outline="white"
        )

        text = self.canvas.create_text(

            x,
            y,

            text=symbols[
                power_type
            ],

            fill="white",

            font=(
                "Arial",
                12,
                "bold"
            )
        )

        self.powerups.append(
            {
                "id": obj,
                "text": text,
                "type": power_type,
                "speed": 3
            }
        )

    def update_powerups(self):

        for power in self.powerups[:]:

            self.canvas.move(
                power["id"],
                0,
                power["speed"]
            )

            self.canvas.move(
                power["text"],
                0,
                power["speed"]
            )

            if self.collision(
                self.player,
                power["id"]
            ):

                self.collect_powerup(
                    power
                )

                continue

            box = self.canvas.bbox(
                power["id"]
            )

            if box and box[1] > HEIGHT:

                self.canvas.delete(
                    power["id"]
                )

                self.canvas.delete(
                    power["text"]
                )

                self.powerups.remove(
                    power
                )

    def collect_powerup(
        self,
        power
    ):

        power_type = power["type"]

        if power_type == "health":

            self.player_hp = min(
                self.player_max_hp,
                self.player_hp + 30
            )

        elif power_type == "shield":

            self.shield = min(
                self.max_shield,
                self.shield + 40
            )

        elif power_type == "weapon":

            self.weapon_level = min(
                3,
                self.weapon_level + 1
            )

        elif power_type == "energy":

            self.special_energy = min(
                100,
                self.special_energy + 40
            )

        self.canvas.delete(
            power["id"]
        )

        self.canvas.delete(
            power["text"]
        )

        self.powerups.remove(
            power
        )

        self.update_hud()

    # ========================================================
    # SPECIAL ATTACK
    # ========================================================

    def special_attack(self):

        if self.special_energy < 100:
            return

        if self.special_cooldown > 0:
            return

        self.special_energy = 0

        self.special_cooldown = 100

        # Huge laser

        laser = self.canvas.create_rectangle(

            WIDTH // 2 - 35,

            0,

            WIDTH // 2 + 35,

            HEIGHT,

            fill="#00ffff",

            outline=""
        )

        self.root.after(
            120,
            lambda:
            self.canvas.delete(
                laser
            )
        )

        # Damage enemies

        for enemy in self.enemies[:]:

            self.kill_enemy(
                enemy
            )

        if self.boss_active and self.boss:

            self.boss["hp"] -= 40

            if self.boss["hp"] <= 0:

                self.kill_boss()

    # ========================================================
    # SCORE / XP
    # ========================================================

    def add_score(
        self,
        amount
    ):

        self.score += amount

        if self.score > self.high_score:

            self.high_score = self.score

            self.save_high_score()

        self.update_hud()

    def add_xp(
        self,
        amount
    ):

        self.xp += amount

        if self.xp >= self.next_level_xp:

            self.level_up()

    def level_up(self):

        self.xp -= self.next_level_xp

        self.level += 1

        self.next_level_xp = int(
            self.next_level_xp * 1.35
        )

        self.player_max_hp += 10

        self.player_hp = self.player_max_hp

        self.shield = self.max_shield

        self.weapon_level = min(
            3,
            self.weapon_level + 1
        )

        self.canvas.create_text(

            WIDTH // 2,

            HEIGHT // 2,

            text=f"LEVEL {self.level}!",

            fill="#ffff00",

            font=(
                "Arial",
                50,
                "bold"
            ),

            tag="level_message"
        )

        self.root.after(
            1200,
            lambda:
            self.canvas.delete(
                "level_message"
            )
        )

        if self.level % 5 == 0:

            self.spawn_boss()

    # ========================================================
    # DAMAGE
    # ========================================================

    def damage_player(
        self,
        amount
    ):

        if self.shield > 0:

            absorbed = min(
                self.shield,
                amount
            )

            self.shield -= absorbed

            amount -= absorbed

        if amount > 0:

            self.player_hp -= amount

        if self.player_hp <= 0:

            self.player_hp = 0

            self.end_game()

        self.update_hud()

    # ========================================================
    # PARTICLES
    # ========================================================

    def create_particle(
        self,
        x,
        y,
        color
    ):

        particle = Particle(
            self.canvas,
            x,
            y,
            color
        )

        self.particles.append(
            particle
        )

    def create_explosion(
        self,
        x,
        y,
        color
    ):

        for _ in range(15):

            self.create_particle(
                x,
                y,
                color
            )

    def update_particles(self):

        for particle in self.particles[:]:

            alive = particle.update()

            if not alive:

                self.particles.remove(
                    particle
                )

    # ========================================================
    # HUD
    # ========================================================

    def create_hud(self):

        self.hud = self.canvas.create_text(

            20,
            20,

            anchor="nw",

            text="",

            fill="white",

            font=(
                "Arial",
                16,
                "bold"
            )
        )

        self.update_hud()

    def update_hud(self):

        if not hasattr(
            self,
            "hud"
        ):
            return

        text = (

            f"SCORE: {self.score}    "

            f"BEST: {self.high_score}\n"

            f"HP: {self.player_hp}/"
            f"{self.player_max_hp}    "

            f"SHIELD: {self.shield}    "

            f"LEVEL: {self.level}\n"

            f"WEAPON: {self.weapon_level}    "

            f"SPECIAL: "
            f"{self.special_energy}%"
        )

        self.canvas.itemconfig(
            self.hud,
            text=text
        )

    # ========================================================
    # INPUT
    # ========================================================

    def key_down(
        self,
        event
    ):

        key = event.keysym

        if self.in_menu:

            if key == "Return":

                self.start_game()

            return

        if self.game_over:

            if key.lower() == "r":

                self.start_game()

            return

        if key.lower() == "p":

            self.paused = not self.paused

        self.keys.add(
            key
        )

        if key == "e":

            self.special_attack()

    def key_up(
        self,
        event
    ):

        self.keys.discard(
            event.keysym
        )

    # ========================================================
    # GAME LOOP
    # ========================================================

    def game_loop(self):

        if self.game_over:

            return

        if not self.paused:

            self.update_stars()

            self.update_player()

            if (
                "space" in self.keys
                or "Space" in self.keys
            ):

                self.shoot()

            self.update_bullets()

            self.update_enemies()

            self.update_enemy_bullets()

            self.update_powerups()

            self.update_particles()

            self.update_boss()

            self.check_collisions()

            if self.shoot_cooldown > 0:

                self.shoot_cooldown -= 1

            if self.special_cooldown > 0:

                self.special_cooldown -= 1

            self.enemy_timer += 1

            spawn_rate = max(
                12,
                45 - self.level * 2
            )

            if (
                self.enemy_timer
                >= spawn_rate
                and not self.boss_active
            ):

                self.spawn_enemy()

                self.enemy_timer = 0

        self.root.after(
            FPS,
            self.game_loop
        )

    # ========================================================
    # GAME OVER
    # ========================================================

    def end_game(self):

        self.game_over = True

        if self.score > self.high_score:

            self.high_score = self.score

            self.save_high_score()

        self.canvas.create_rectangle(

            0,
            0,
            WIDTH,
            HEIGHT,

            fill="#000000",

            stipple="gray50",

            outline="",

            tag="gameover"
        )

        self.canvas.create_text(

            WIDTH // 2,

            HEIGHT // 2 - 70,

            text="GAME OVER",

            fill="#ff3355",

            font=(
                "Arial",
                55,
                "bold"
            ),

            tag="gameover"
        )

        self.canvas.create_text(

            WIDTH // 2,

            HEIGHT // 2,

            text=f"SCORE: {self.score}",

            fill="white",

            font=(
                "Arial",
                25,
                "bold"
            ),

            tag="gameover"
        )

        self.canvas.create_text(

            WIDTH // 2,

            HEIGHT // 2 + 45,

            text=f"BEST: {self.high_score}",

            fill="#ffd700",

            font=(
                "Arial",
                20,
                "bold"
            ),

            tag="gameover"
        )

        self.canvas.create_text(

            WIDTH // 2,

            HEIGHT // 2 + 100,

            text="PRESS R TO PLAY AGAIN",

            fill="#00ffff",

            font=(
                "Arial",
                18,
                "bold"
            ),

            tag="gameover"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    root = tk.Tk()

    game = SpaceBattlePro(
        root
    )

    root.mainloop()


if __name__ == "__main__":

    main()

















   # وقتی بازی اومد اینتر بزن شروع میشه