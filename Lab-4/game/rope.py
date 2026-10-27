import math
import pygame


class Rope:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_y = screen_height // 2
        self.marker_x = screen_width // 2

        self.left_win_x = 180
        self.right_win_x = screen_width - 180
        self.pull_step = 12

        # Task 3: Dynamic tension, hum vibration & sag physics
        self.struggle_intensity = 0.3    # 0.0 (slack/sagging) to 1.0 (taut & vibrating hum)

    def trigger_struggle(self, amount=0.35):
        """Boost tension when pulls occur."""
        self.struggle_intensity = min(1.0, self.struggle_intensity + amount)

    def update(self):
        """Decay tension smoothly towards resting level."""
        self.struggle_intensity = max(0.1, self.struggle_intensity - 0.012)

    def pull_left(self, strength=1.0):
        self.marker_x -= int(self.pull_step * strength)
        self.trigger_struggle(0.35 * strength)

    def pull_right(self, strength=1.0):
        self.marker_x += int(self.pull_step * strength)
        self.trigger_struggle(0.35 * strength)

    def check_winner(self):
        if self.marker_x <= self.left_win_x:
            return "PLAYER"
        if self.marker_x >= self.right_win_x:
            return "COMPUTER"
        return None

    def reset(self):
        self.marker_x = float(self.screen_width // 2)
        self.struggle_intensity = 0.3

    def render(self, surface):
        ticks = pygame.time.get_ticks()

        # Task 3: Dynamic Rope Vibration Hum & Sag Curve
        # Low tension -> rope sags downward between pullers
        # High tension -> rope pulls taut and vibrates with high-tension hum
        start_x = 90
        end_x = self.screen_width - 90
        num_segments = 48

        points = []
        center_flag_y = self.center_y

        sag_amplitude = (1.0 - self.struggle_intensity) * 16.0
        vibe_amplitude = self.struggle_intensity * 4.5

        for i in range(num_segments + 1):
            px = start_x + (end_x - start_x) * (i / num_segments)
            # Parabolic sag calculation: maximum at midpoint
            norm_span = (px - start_x) / (end_x - start_x)
            sag = 4.0 * norm_span * (1.0 - norm_span) * sag_amplitude

            # High-tension vibrating hum calculation
            # Standing wave pattern with rapid oscillation
            wave = math.sin(math.pi * norm_span) * math.sin(ticks * 0.065 + i * 0.3) * vibe_amplitude

            py = self.center_y + sag + wave
            points.append((int(px), int(py)))

            if abs(px - self.marker_x) < (end_x - start_x) / num_segments:
                center_flag_y = py

        # Draw outer thick rope shadow / braid
        pygame.draw.lines(surface, (120, 85, 50), False, points, 12)
        # Draw main rope core
        pygame.draw.lines(surface, (190, 150, 100), False, points, 8)
        # Draw inner tension highlight
        highlight_points = [(p[0], p[1] - 1) for p in points]
        pygame.draw.lines(surface, (220, 185, 135), False, points, 3)

        # Win boundary indicators
        pygame.draw.line(
            surface,
            (50, 200, 50),
            (self.left_win_x, self.center_y - 40),
            (self.left_win_x, self.center_y + 40),
            4
        )
        pygame.draw.line(
            surface,
            (200, 50, 50),
            (self.right_win_x, self.center_y - 40),
            (self.right_win_x, self.center_y + 40),
            4
        )

        # Center neutral line
        pygame.draw.line(
            surface,
            (120, 120, 120),
            (self.screen_width // 2, self.center_y - 20),
            (self.screen_width // 2, self.center_y + 20),
            2
        )

        # Center red marker flag, dynamically following the rope's current y height
        flag_rect = pygame.Rect(int(self.marker_x) - 12, int(center_flag_y) - 24, 24, 48)
        pygame.draw.rect(surface, (230, 40, 40), flag_rect, border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255), flag_rect, width=2, border_radius=4)
