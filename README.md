# Stickman Samurai Duel Animation

A procedurally-generated animation of two stickmen engaged in a samurai-style duel.

## Features

- **Two Stickman Fighters**: Red fighter (right side) and Blue fighter (left side)
- **Dynamic Actions**: 
  - Idle stance
  - Attack with sword thrust
  - Defensive block
  - Dodge maneuvers
- **Animation Cycles**: 4-second combat cycles with alternating offensive and defensive sequences
- **Video Output**: MP4 format at 30 FPS

## Combat Sequence

The duel follows a repeating pattern:

1. **Frames 0-30**: Red attacks, Blue defends
2. **Frames 30-40**: Red idles, Blue dodges
3. **Frames 40-70**: Red defends, Blue attacks
4. **Frames 70-80**: Red dodges, Blue idles
5. **Frames 80-120**: Both idle, preparing for next cycle

## Requirements

- Python 3.6+
- opencv-python
- Pillow (PIL)
- numpy

## Installation

```bash
pip install opencv-python pillow numpy
```

## Usage

```bash
python3 stickman_duel.py
```

This will generate `stickman_duel.mp4` in the current directory.

## Output

- **Resolution**: 800x600 pixels
- **Duration**: 15 seconds
- **Frame Rate**: 30 FPS
- **Total Frames**: 450
- **Format**: MP4

## Customization

You can customize the animation by modifying parameters in the `main()` function:

```python
anim = DuelAnimation(
    width=800,      # Video width in pixels
    height=600,     # Video height in pixels
    fps=30,         # Frames per second
    duration=15     # Duration in seconds
)
```

## Technical Details

- **StickFigure class**: Handles drawing individual stickmen with different poses
- **DuelAnimation class**: Manages the overall animation sequence and video generation
- Frame-based action system allows for smooth transitions and choreographed combat

## License

MIT
