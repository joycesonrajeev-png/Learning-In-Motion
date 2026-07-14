#!/usr/bin/env python3
"""
Stickman Samurai Duel Animation
Creates an animated video of two stickmen engaging in a samurai-style duel.
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw
import math
import os

class StickFigure:
    """Represents a stickman figure with limbs and sword."""

    def __init__(self, x, y, direction=1):
        self.x = x
        self.y = y
        self.direction = direction  # 1 for right, -1 for left
        self.head_radius = 15
        self.body_length = 40
        self.limb_length = 35

    def draw(self, draw, color, frame_num, action="idle"):
        """Draw the stickman with animation based on action."""
        # Head
        head_x, head_y = self.x, self.y
        draw.ellipse([head_x - self.head_radius, head_y - self.head_radius,
                      head_x + self.head_radius, head_y + self.head_radius],
                     outline=color, width=2)

        # Body
        body_top_y = head_y + self.head_radius
        body_bottom_y = body_top_y + self.body_length
        draw.line([head_x, body_top_y, head_x, body_bottom_y], fill=color, width=2)

        # Animation based on action
        if action == "idle":
            self._draw_idle(draw, color, head_x, body_top_y, body_bottom_y)
        elif action == "attack":
            self._draw_attack(draw, color, head_x, body_top_y, body_bottom_y, frame_num)
        elif action == "defend":
            self._draw_defend(draw, color, head_x, body_top_y, body_bottom_y, frame_num)
        elif action == "dodge":
            self._draw_dodge(draw, color, head_x, body_top_y, body_bottom_y, frame_num)

    def _draw_idle(self, draw, color, head_x, body_top_y, body_bottom_y):
        """Draw idle stance with arms and legs."""
        # Arms
        arm_y = body_top_y + 10
        draw.line([head_x, arm_y, head_x - self.direction * self.limb_length, arm_y - 5],
                  fill=color, width=2)
        draw.line([head_x, arm_y, head_x + self.direction * self.limb_length, arm_y - 5],
                  fill=color, width=2)

        # Legs
        draw.line([head_x, body_bottom_y, head_x - self.direction * 15, body_bottom_y + self.limb_length],
                  fill=color, width=2)
        draw.line([head_x, body_bottom_y, head_x + self.direction * 15, body_bottom_y + self.limb_length],
                  fill=color, width=2)

    def _draw_attack(self, draw, color, head_x, body_top_y, body_bottom_y, frame_num):
        """Draw attacking pose with sword thrust."""
        arm_y = body_top_y + 5
        sword_length = 60

        # Weapon arm (extended with sword)
        sword_tip_x = head_x + self.direction * (self.limb_length + sword_length)
        draw.line([head_x, arm_y, sword_tip_x, arm_y], fill=color, width=2)
        # Sword
        draw.line([head_x + self.direction * self.limb_length, arm_y - 3,
                   sword_tip_x, arm_y + 3], fill=color, width=3)

        # Non-weapon arm (back)
        draw.line([head_x, arm_y, head_x - self.direction * (self.limb_length // 2), arm_y + 10],
                  fill=color, width=2)

        # Legs (lunging stance)
        draw.line([head_x, body_bottom_y, head_x - self.direction * 20, body_bottom_y + self.limb_length],
                  fill=color, width=2)
        draw.line([head_x, body_bottom_y, head_x + self.direction * 5, body_bottom_y + self.limb_length - 5],
                  fill=color, width=2)

    def _draw_defend(self, draw, color, head_x, body_top_y, body_bottom_y, frame_num):
        """Draw defensive pose with sword blocking."""
        arm_y = body_top_y + 5

        # Weapon arm (raised for defense)
        defend_x = head_x + self.direction * (self.limb_length // 2)
        defend_y = body_top_y - 15
        draw.line([head_x, arm_y, defend_x, defend_y], fill=color, width=2)
        # Sword (diagonal block)
        draw.line([defend_x - 5, defend_y - 10, defend_x + 20, defend_y + 20],
                  fill=color, width=3)

        # Non-weapon arm (guard)
        draw.line([head_x, arm_y, head_x - self.direction * 20, arm_y + 5],
                  fill=color, width=2)

        # Stable legs
        draw.line([head_x, body_bottom_y, head_x - self.direction * 12, body_bottom_y + self.limb_length],
                  fill=color, width=2)
        draw.line([head_x, body_bottom_y, head_x + self.direction * 12, body_bottom_y + self.limb_length],
                  fill=color, width=2)

    def _draw_dodge(self, draw, color, head_x, body_top_y, body_bottom_y, frame_num):
        """Draw dodging pose."""
        arm_y = body_top_y + 10

        # Arms up for balance
        draw.line([head_x, arm_y, head_x - self.direction * self.limb_length, arm_y - 20],
                  fill=color, width=2)
        draw.line([head_x, arm_y, head_x + self.direction * self.limb_length, arm_y - 10],
                  fill=color, width=2)

        # Legs in dodge position
        draw.line([head_x, body_bottom_y, head_x - self.direction * 5, body_bottom_y + self.limb_length],
                  fill=color, width=2)
        draw.line([head_x, body_bottom_y, head_x + self.direction * 25, body_bottom_y + self.limb_length - 10],
                  fill=color, width=2)


class DuelAnimation:
    """Creates a samurai duel animation."""

    def __init__(self, width=800, height=600, fps=30, duration=15):
        self.width = width
        self.height = height
        self.fps = fps
        self.duration = duration
        self.total_frames = fps * duration

    def generate_frames(self):
        """Generate all frames of the animation."""
        frames = []

        for frame_num in range(self.total_frames):
            frame = Image.new('RGB', (self.width, self.height), color='white')
            draw = ImageDraw.Draw(frame)

            # Draw background elements
            self._draw_background(draw, frame_num)

            # Create fighters
            fighter1 = StickFigure(self.width // 3, self.height // 2, direction=1)
            fighter2 = StickFigure(2 * self.width // 3, self.height // 2, direction=-1)

            # Determine actions based on frame
            action1, action2 = self._get_actions(frame_num)

            # Update positions for movement
            if action1 == "attack":
                fighter1.x += 3
            elif action1 == "dodge":
                fighter1.y += 5

            if action2 == "attack":
                fighter2.x -= 3
            elif action2 == "dodge":
                fighter2.y -= 5

            # Draw fighters
            fighter1.draw(draw, 'red', frame_num, action1)
            fighter2.draw(draw, 'blue', frame_num, action2)

            # Draw scene number
            self._draw_text(draw, frame_num)

            frames.append(np.array(frame))

        return frames

    def _draw_background(self, draw, frame_num):
        """Draw background elements."""
        # Ground line
        draw.line([0, self.height - 100, self.width, self.height - 100],
                  fill='black', width=2)

        # Simple landscape
        draw.polygon([0, self.height - 100, self.width, self.height - 100,
                      self.width, self.height, 0, self.height],
                     fill='tan', outline='black')

        # Sun/background effect
        draw.ellipse([self.width - 150, 20, self.width - 50, 120],
                     fill='yellow', outline='orange')

    def _get_actions(self, frame_num):
        """Determine the action for each fighter based on frame number."""
        frame_in_cycle = frame_num % 120  # 4-second cycle at 30fps

        # Fighter 1 (red) attacks, fighter 2 (blue) defends/dodges
        if frame_in_cycle < 30:
            return "attack", "defend"
        elif frame_in_cycle < 40:
            return "idle", "dodge"
        elif frame_in_cycle < 70:
            return "defend", "attack"
        elif frame_in_cycle < 80:
            return "dodge", "idle"
        else:
            return "idle", "idle"

    def _draw_text(self, draw, frame_num):
        """Draw frame counter and title."""
        seconds = frame_num / self.fps
        draw.text((10, 10), f"SAMURAI DUEL - {seconds:.1f}s", fill='black')

    def create_video(self, output_path='stickman_duel.mp4'):
        """Generate all frames and create video file."""
        print(f"Generating {self.total_frames} frames...")
        frames = self.generate_frames()

        print(f"Creating video: {output_path}")
        # Use OpenCV to write video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))

        for i, frame in enumerate(frames):
            if (i + 1) % 30 == 0:
                print(f"  Frame {i + 1}/{self.total_frames}")
            # Convert RGB to BGR for OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame_bgr)

        out.release()
        print(f"✓ Video saved: {output_path}")
        return output_path


def main():
    """Main function to create the animation."""
    # Create animation (15 seconds)
    anim = DuelAnimation(width=800, height=600, fps=30, duration=15)
    anim.create_video('stickman_duel.mp4')


if __name__ == '__main__':
    main()
