import pygame


class Puller:
    """Represents a puller character anchor on either side of the rope with dynamic leaning animation."""

    def __init__(self, x, y, color, label):
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.is_left_side = (x < 400)
        self.font = pygame.font.SysFont(None, 24)

        # Task 3: Leaning animation & momentum state
        self.lean_angle = 0.0      # Current rendered lean offset
        self.target_lean = 0.0     # Target lean offset
        self.momentum = 0.0        # Exertion/struggle intensity

    def apply_pull_impulse(self, strength=1.0):
        """Trigger backward lean when pulling with momentum."""
        self.momentum = min(1.0, self.momentum + 0.35 * strength)
        # Left puller leans backward to the left (negative x offset)
        # Right puller leans backward to the right (positive x offset)
        direction = -1.0 if self.is_left_side else 1.0
        self.target_lean = direction * min(32.0, 16.0 + 10.0 * strength)

    def apply_dragged_impulse(self):
        """Slight forward stumble when opponent pulls aggressively."""
        # When dragged, lean forward toward the center
        forward_dir = 1.0 if self.is_left_side else -1.0
        self.target_lean = forward_dir * 10.0

    def update(self):
        """Update animation physics with smooth damping."""
        # Lerp towards target lean
        self.lean_angle += (self.target_lean - self.lean_angle) * 0.22
        # Gradually relax target lean towards rest position
        self.target_lean *= 0.88
        self.momentum = max(0.0, self.momentum - 0.02)

    def render(self, surface):
        """Draw avatar with dynamic backward leaning posture based on pulling momentum."""
        lean = self.lean_angle

        # Feet remain anchored
        foot_y = self.y + 35
        left_foot_x = self.x - 16
        right_foot_x = self.x + 16

        # Torso leans backwards or forwards
        shoulder_y = self.y - 30
        left_shoulder_x = self.x - 18 + lean
        right_shoulder_x = self.x + 18 + lean

        # Draw torso as leaning polygon
        torso_points = [
            (left_foot_x, foot_y),
            (right_foot_x, foot_y),
            (right_shoulder_x, shoulder_y),
            (left_shoulder_x, shoulder_y)
        ]
        pygame.draw.polygon(surface, self.color, torso_points)
        pygame.draw.polygon(surface, (255, 255, 255), torso_points, width=2)

        # Head position follows torso lean
        head_x = int(self.x + lean * 1.25)
        head_y = int(self.y - 48)
        pygame.draw.circle(surface, (240, 210, 180), (head_x, head_y), 16)
        pygame.draw.circle(surface, (40, 40, 40), (head_x, head_y), 16, width=2)

        # Arms holding rope towards center
        hand_x = self.x + (28 if self.is_left_side else -28) + int(lean * 0.5)
        hand_y = self.y - 2
        pygame.draw.line(surface, self.color, (int((left_shoulder_x + right_shoulder_x) / 2), shoulder_y + 12), (hand_x, hand_y), 6)
        pygame.draw.circle(surface, (240, 210, 180), (hand_x, hand_y), 6)

        # Exertion sweat/strain glow when pulling hard
        if self.momentum > 0.4:
            sweat_color = (120, 220, 255)
            pygame.draw.circle(surface, sweat_color, (head_x + (-12 if self.is_left_side else 12), head_y - 10), 3)

        # Name / control tag
        label_surf = self.font.render(self.label, True, (240, 240, 240))
        surface.blit(label_surf, (self.x - label_surf.get_width() // 2, self.y + 45))
