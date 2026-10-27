import random
import pygame
from game.rope import Rope
from game.player import Puller


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rope = Rope(width, height)
        self.player = Puller(90, height // 2, (50, 120, 220), "PLAYER (A/D)")
        self.computer = Puller(width - 90, height // 2, (220, 80, 50), "COMPUTER")

        self.last_key = None
        self.is_pull_locked = False
        self.winner = None
        self.game_state = "PLAYING"

        # AI pulling & dynamic panic surge parameters (Task 2)
        self.base_computer_cooldown = 180
        self.computer_pull_cooldown = 180
        self.last_computer_pull = pygame.time.get_ticks()
        self.is_panic_surge = False
        self.panic_level = 0.0

        # Match timer & sudden death mode parameters (Task 4)
        self.match_time_limit = 45.0     # 45 seconds threshold
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed_sec = 0.0
        self.is_sudden_death = False

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 30)
        self.font_small = pygame.font.SysFont(None, 22)

    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        # Task 1 Fix: Alternating Input Deadlock Bug
        # Decouple pull registration from KEYUP lockout so rapid and overlapping
        # key presses (A and D) alternate smoothly without freezing.
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_d):
                if event.key != self.last_key:
                    # Task 4: 2x power multiplier under Sudden Death
                    pull_multiplier = 2.0 if self.is_sudden_death else 1.0
                    self.rope.pull_left(1.0 * pull_multiplier)
                    self.last_key = event.key
                    self.is_pull_locked = False

                    # Task 3: Backward leaning animation & struggle intensity
                    self.player.apply_pull_impulse(1.0 * pull_multiplier)
                    self.computer.apply_dragged_impulse()

    def update(self):
        if self.game_state != "PLAYING":
            return

        now = pygame.time.get_ticks()

        # Task 4: Live match timer update and sudden death check
        self.elapsed_sec = (now - self.start_ticks) / 1000.0
        if self.elapsed_sec >= self.match_time_limit:
            self.is_sudden_death = True

        # Task 3: Update physics & animation states
        self.rope.update()
        self.player.update()
        self.computer.update()

        # Task 2: Dynamic AI Panic Surges
        center_x = self.width / 2.0
        left_threshold = float(self.rope.left_win_x)
        if self.rope.marker_x < center_x:
            self.panic_level = max(0.0, min(1.0, (center_x - self.rope.marker_x) / (center_x - left_threshold)))
        else:
            self.panic_level = 0.0

        if self.panic_level > 0.15:
            self.is_panic_surge = True
            self.computer_pull_cooldown = max(65, int(self.base_computer_cooldown - (self.panic_level * 115)))
        else:
            self.is_panic_surge = False
            self.computer_pull_cooldown = self.base_computer_cooldown

        # Computer pulling cadence
        if now - self.last_computer_pull >= self.computer_pull_cooldown:
            if self.is_panic_surge:
                surge_boost = self.panic_level * 1.2
                computer_variance = random.uniform(1.0 + surge_boost, 1.5 + surge_boost)
            else:
                computer_variance = random.uniform(0.7, 1.2)

            # Task 4: 2x power multiplier across all actions during Sudden Death
            pull_multiplier = 2.0 if self.is_sudden_death else 1.0
            actual_pull = computer_variance * pull_multiplier

            self.rope.pull_right(actual_pull)
            self.computer.apply_pull_impulse(actual_pull)
            self.player.apply_dragged_impulse()
            self.last_computer_pull = now

        result = self.rope.check_winner()
        if result:
            self.winner = result
            self.game_state = "GAME_OVER"

    def reset(self):
        self.rope.reset()
        self.player.lean_angle = 0.0
        self.player.target_lean = 0.0
        self.computer.lean_angle = 0.0
        self.computer.target_lean = 0.0
        self.last_key = None
        self.is_pull_locked = False
        self.winner = None
        self.game_state = "PLAYING"
        self.computer_pull_cooldown = self.base_computer_cooldown
        self.is_panic_surge = False
        self.panic_level = 0.0
        self.last_computer_pull = pygame.time.get_ticks()
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed_sec = 0.0
        self.is_sudden_death = False

    def render(self, screen):
        screen.fill((30, 32, 36))

        # Mud pit in center
        mud_rect = pygame.Rect(self.width // 2 - 120, self.height // 2 - 80, 240, 160)
        pygame.draw.rect(screen, (45, 38, 30), mud_rect, border_radius=12)

        self.rope.render(screen)
        self.player.render(screen)
        self.computer.render(screen)

        # Task 4: Live Match Timer & Sudden Death banner HUD
        timer_box = pygame.Rect(self.width // 2 - 140, 8, 280, 28)
        pygame.draw.rect(screen, (20, 22, 26), timer_box, border_radius=6)
        pygame.draw.rect(screen, (70, 75, 85), timer_box, width=1, border_radius=6)

        if not self.is_sudden_death:
            timer_text = f"MATCH TIMER: {self.elapsed_sec:.1f}s / {self.match_time_limit:.0f}s"
            timer_color = (240, 240, 240) if self.elapsed_sec < 35 else (255, 180, 60)
        else:
            # Pulsing gold/red Sudden Death indicator
            ticks = pygame.time.get_ticks()
            flash = (ticks // 300) % 2 == 0
            timer_text = f"SUDDEN DEATH: {self.elapsed_sec:.1f}s (2X POWER!)"
            timer_color = (255, 60, 60) if flash else (255, 215, 0)

        timer_surf = self.font_small.render(timer_text, True, timer_color)
        screen.blit(timer_surf, (self.width // 2 - timer_surf.get_width() // 2, 13))

        # Instructions / Next Key Prompt
        next_hint = " [D]" if self.last_key == pygame.K_a else (" [A]" if self.last_key == pygame.K_d else " [A or D]")
        inst_surf = self.font_small.render(
            f"Alternate [A] and [D] rapidly to pull! Next required: {next_hint}", True, (200, 200, 200)
        )
        screen.blit(inst_surf, (self.width // 2 - inst_surf.get_width() // 2, 42))

        # Task 2: Visual indicator for Dynamic AI Panic Surge
        if self.is_panic_surge and self.game_state == "PLAYING":
            surge_color = (255, max(50, int(180 - self.panic_level * 130)), 30)
            surge_text = f"! AI PANIC SURGE ! Cadence: {self.computer_pull_cooldown}ms (+{int(self.panic_level*100)}% Danger)"
            surge_surf = self.font_small.render(surge_text, True, surge_color)
            screen.blit(surge_surf, (self.width // 2 - surge_surf.get_width() // 2, 68))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            win_text = f"{self.winner} WINS!"
            color = (80, 220, 80) if self.winner == "PLAYER" else (240, 80, 80)
            text_surf = self.font_big.render(win_text, True, color)
            screen.blit(
                text_surf,
                (self.width // 2 - text_surf.get_width() // 2, self.height // 2 - 50)
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again", True, (240, 240, 240)
            )
            screen.blit(
                restart_surf,
                (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 10)
            )
