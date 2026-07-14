#!/usr/bin/env python3
"""
Enhanced Stickman Samurai Duel Animation
Creates a more dynamic and visually impressive samurai duel video.
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math

class Particle:
    """Represents a particle effect (dust, blood, etc)."""
    def __init__(self, x, y, vx, vy, color, life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = life
        self.max_life = life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3  # gravity
        self.life -= 1

    def is_alive(self):
        return self.life > 0

    def draw(self, draw):
        alpha = int(255 * (self.life / self.max_life))
        size = max(1, int(4 * (self.life / self.max_life)))
        draw.ellipse([self.x - size, self.y - size, self.x + size, self.y + size],
                     fill=self.color)


class EnhancedStickFigure:
    """Enhanced stickman with better proportions and details."""

    def __init__(self, x, y, direction=1):
        self.x = x
        self.y = y
        self.direction = direction
        self.head_radius = 12
        self.body_length = 35
        self.limb_length = 30
        self.velocity_x = 0
        self.particles = []

    def update_position(self, target_x, speed=2):
        """Update position towards target."""
        if abs(self.x - target_x) > 5:
            self.x += (target_x - self.x) * 0.05

    def draw(self, draw, color, frame_num, action="idle"):
        """Draw the enhanced stickman."""
        # Head with eyes
        head_x, head_y = self.x, self.y
        draw.ellipse([head_x - self.head_radius, head_y - self.head_radius,
                      head_x + self.head_radius, head_y + self.head_radius],
                     outline=color, width=3)

        # Eyes
        eye_offset = 5
        eye_y = head_y - 3
        draw.ellipse([head_x - eye_offset - 2, eye_y - 2,
                      head_x - eye_offset + 2, eye_y + 2], fill=color)
        draw.ellipse([head_x + eye_offset - 2, eye_y - 2,
                      head_x + eye_offset + 2, eye_y + 2], fill=color)

        # Body (thicker)
        body_top_y = head_y + self.head_radius
        body_bottom_y = body_top_y + self.body_length
        draw.line([head_x, body_top_y, head_x, body_bottom_y], fill=color, width=3)

        # Draw based on action
        if action == "idle":
            self._draw_idle(draw, color, head_x, body_top_y, body_bottom_y)
        elif action == "attack":
            self._draw_attack(draw, color, head_x, body_top_y, body_bottom_y)
        elif action == "defend":
            self._draw_defend(draw, color, head_x, body_top_y, body_bottom_y)
        elif action == "dodge_left":
            self._draw_dodge_left(draw, color, head_x, body_top_y, body_bottom_y)
        elif action == "dodge_right":
            self._draw_dodge_right(draw, color, head_x, body_top_y, body_bottom_y)
        elif action == "hit":
            self._draw_hit(draw, color, head_x, body_top_y, body_bottom_y)

    def _draw_idle(self, draw, color, head_x, body_top_y, body_bottom_y):
        """Idle stance."""
        arm_y = body_top_y + 8
        draw.line([head_x, arm_y, head_x - self.direction * self.limb_length,
                   arm_y - 8], fill=color, width=2)
        draw.line([head_x, arm_y, head_x + self.direction * self.limb_length * 0.7,
                   arm_y + 5], fill=color, width=2)

        draw.line([head_x, body_bottom_y, head_x - self.direction * 12,
                   body_bottom_y + self.limb_length], fill=color, width=2)
        draw.line([head_x, body_bottom_y, head_x + self.direction * 12,
                   body_bottom_y + self.limb_length], fill=color, width=2)

    def _draw_attack(self, draw, color, head_x, body_top_y, body_bottom_y):
        """Aggressive attack with sword."""
        arm_y = body_top_y + 5
        sword_length = 55

        # Sword arm extended
        sword_tip_x = head_x + self.direction * (self.limb_length + sword_length)
        draw.line([head_x, arm_y, sword_tip_x, arm_y], fill=color, width=2)

        # Sword blade
        draw.line([head_x + self.direction * self.limb_length, arm_y - 4,
                   sword_tip_x, arm_y + 4], fill='silver', width=4)

        # Back arm
        draw.line([head_x, arm_y, head_x - self.direction * 20, arm_y + 15],
                  fill=color, width=2)

        # Lunging legs
        draw.line([head_x, body_bottom_y, head_x - self.direction * 25,
                   body_bottom_y + self.limb_length], fill=color, width=2)
        draw.line([head_x, body_bottom_y, head_x + self.direction * 8,
                   body_bottom_y + self.limb_length - 8], fill=color, width=2)

    def _draw_defend(self, draw, color, head_x, body_top_y, body_bottom_y):
        """Defensive block position."""
        arm_y = body_top_y + 5

        # Defensive sword angle
        block_x = head_x + self.direction * self.limb_length * 0.6
        block_y = body_top_y - 10
        draw.line([head_x, arm_y, block_x, block_y], fill=color, width=2)

        # Sword at angle
        draw.line([block_x - 3, block_y - 12, block_x + 25, block_y + 15],
                  fill='silver', width=4)

        # Guard arm
        draw.line([head_x, arm_y, head_x - self.direction * 25, arm_y + 8],
                  fill=color, width=2)

        # Stable stance
        draw.line([head_x, body_bottom_y, head_x - self.direction * 15,
                   body_bottom_y + self.limb_length], fill=color, width=2)
        draw.line([head_x, body_bottom_y, head_x + self.direction * 15,
                   body_bottom_y + self.limb_length], fill=color, width=2)

    def _draw_dodge_left(self, draw, color, head_x, body_top_y, body_bottom_y):
        """Dodging to the left."""
        arm_y = body_top_y + 8
        draw.line([head_x, arm_y, head_x - self.limb_length * 1.2, arm_y - 15],
                  fill=color, width=2)
        draw.line([head_x, arm_y, head_x + self.limb_length * 0.8, arm_y - 5],
                  fill=color, width=2)

        draw.line([head_x, body_bottom_y, head_x - 30, body_bottom_y + self.limb_length - 10],
                  fill=color, width=2)
        draw.line([head_x, body_bottom_y, head_x + 5, body_bottom_y + self.limb_length],
                  fill=color, width=2)

    def _draw_dodge_right(self, draw, color, head_x, body_top_y, body_bottom_y):
        """Dodging to the right."""
        arm_y = body_top_y + 8
        draw.line([head_x, arm_y, head_x + self.limb_length * 1.2, arm_y - 15],
                  fill=color, width=2)
        draw.line([head_x, arm_y, head_x - self.limb_length * 0.8, arm_y - 5],
                  fill=color, width=2)

        draw.line([head_x, body_bottom_y, head_x + 30, body_bottom_y + self.limb_length - 10],
                  fill=color, width=2)
        draw.line([head_x, body_bottom_y, head_x - 5, body_bottom_y + self.limb_length],
                  fill=color, width=2)

    def _draw_hit(self, draw, color, head_x, body_top_y, body_bottom_y):
        """Hit/staggered position."""
        arm_y = body_top_y + 10
        draw.line([head_x, arm_y, head_x - self.direction * 15, arm_y - 20],
                  fill=color, width=2)
        draw.line([head_x, arm_y, head_x + self.direction * 10, arm_y - 5],
                  fill=color, width=2)

        draw.line([head_x, body_bottom_y, head_x - self.direction * 20,
                   body_bottom_y + self.limb_length], fill=color, width=2)
        draw.line([head_x, body_bottom_y, head_x + self.direction * 5,
                   body_bottom_y + self.limb_length + 5], fill=color, width=2)

    def add_particle(self, x, y, vx, vy, color, life=20):
        """Add a particle effect."""
        self.particles.append(Particle(x, y, vx, vy, color, life))

    def update_particles(self):
        """Update all particles."""
        for p in self.particles[:]:
            p.update()
            if not p.is_alive():
                self.particles.remove(p)

    def draw_particles(self, draw):
        """Draw all particles."""
        for p in self.particles:
            p.draw(draw)


class DuelAnimationEnhanced:
    """Enhanced duel animation with better choreography."""

    def __init__(self, width=1000, height=700, fps=60, duration=20):
        self.width = width
        self.height = height
        self.fps = fps
        self.duration = duration
        self.total_frames = fps * duration

    def generate_frames(self):
        """Generate all frames."""
        frames = []

        for frame_num in range(self.total_frames):
            frame = Image.new('RGB', (self.width, self.height), color='#1a1a1a')
            draw = ImageDraw.Draw(frame)

            # Background
            self._draw_background(draw, frame_num)

            # Create fighters
            fighter1 = EnhancedStickFigure(self.width // 3, self.height // 2 + 50, direction=1)
            fighter2 = EnhancedStickFigure(2 * self.width // 3, self.height // 2 + 50, direction=-1)

            # Get actions
            action1, action2, impact = self._get_choreography(frame_num)

            # Move fighters
            if action1 == "attack":
                fighter1.x += 4
            elif action1 in ["dodge_left", "dodge_right"]:
                fighter1.x += (2 if action1 == "dodge_right" else -2)

            if action2 == "attack":
                fighter2.x -= 4
            elif action2 in ["dodge_left", "dodge_right"]:
                fighter2.x += (2 if action2 == "dodge_left" else -2)

            # Draw fighters
            fighter1.draw(draw, '#ff4444', frame_num, action1)
            fighter2.draw(draw, '#4444ff', frame_num, action2)

            # Draw impact effects
            if impact:
                self._draw_impact(draw, impact['x'], impact['y'])

            # Draw UI
            self._draw_ui(draw, frame_num)

            frames.append(np.array(frame))

        return frames

    def _draw_background(self, draw, frame_num):
        """Draw background with dojo aesthetic."""
        # Ground
        draw.rectangle([0, self.height - 120, self.width, self.height],
                       fill='#2a2a2a')

        # Wood texture
        for i in range(0, self.width, 40):
            draw.line([i, self.height - 120, i + 20, self.height - 120],
                      fill='#1a1a1a', width=1)

        # Moon/sun
        draw.ellipse([self.width - 200, 50, self.width - 50, 200],
                     fill='#ffcc00', outline='#ff9900')

        # Mountains silhouette
        points = [(0, self.height - 200),
                  (self.width // 4, self.height - 100),
                  (self.width // 2, self.height - 150),
                  (3 * self.width // 4, self.height - 80),
                  (self.width, self.height - 120),
                  (self.width, self.height - 120),
                  (0, self.height - 120)]
        draw.polygon(points, fill='#1a1a1a')

    def _get_choreography(self, frame_num):
        """Define the fight choreography."""
        cycle = frame_num % 180  # 3-second cycles at 60fps

        impact = None

        if cycle < 40:  # Fighter 1 attacks
            action1 = "attack"
            action2 = "defend"
            if cycle == 35:
                impact = {'x': self.width * 0.65, 'y': self.height // 2 + 40}
        elif cycle < 50:  # Recovery
            action1 = "idle"
            action2 = "defend"
        elif cycle < 55:  # Fighter 2 dodges
            action1 = "idle"
            action2 = "dodge_left"
        elif cycle < 95:  # Fighter 2 attacks
            action1 = "defend"
            action2 = "attack"
            if cycle == 90:
                impact = {'x': self.width * 0.35, 'y': self.height // 2 + 40}
        elif cycle < 105:  # Recovery
            action1 = "defend"
            action2 = "idle"
        elif cycle < 110:  # Fighter 1 dodges
            action1 = "dodge_right"
            action2 = "idle"
        else:  # Both idle, reset
            action1 = "idle"
            action2 = "idle"

        return action1, action2, impact

    def _draw_impact(self, draw, x, y):
        """Draw impact effect."""
        # Impact circle
        for r in range(20, 5, -3):
            alpha = int(255 * (1 - (r - 5) / 15))
            draw.ellipse([x - r, y - r, x + r, y + r],
                         outline='#ffaa00', width=2)

        # Sparks
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            sx = x + math.cos(rad) * 20
            sy = y + math.sin(rad) * 20
            draw.line([x, y, sx, sy], fill='#ffaa00', width=2)

    def _draw_ui(self, draw, frame_num):
        """Draw UI elements."""
        seconds = frame_num / self.fps
        draw.text((20, 20), f"SAMURAI DUEL - {seconds:.1f}s",
                  fill='#cccccc')

        # Score/round indicator
        draw.text((self.width - 200, 20), "ROUND 1",
                  fill='#cccccc')


def main():
    """Main function."""
    print("Creating enhanced stickman duel animation...")
    anim = DuelAnimationEnhanced(width=1000, height=700, fps=60, duration=20)

    print(f"Generating {anim.total_frames} frames...")
    frames = anim.generate_frames()

    output_path = 'stickman_duel_enhanced.mp4'
    print(f"Writing video: {output_path}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, anim.fps, (anim.width, anim.height))

    for i, frame in enumerate(frames):
        if (i + 1) % 60 == 0:
            print(f"  Frame {i + 1}/{anim.total_frames}")
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)

    out.release()
    print(f"✓ Video saved: {output_path}")


if __name__ == '__main__':
    main()
