# Lab 4: VibeCoding - Tug of War Repair Lab

**Student Name:** SURYA A BHAT  
**SRN:** PES1UG24AM296  
**Course:** Software Engineering (UE24CS252AA)  
**Assigned Source Repository:** [SETAPESU26/56_tug_of_war](https://github.com/SETAPESU26/56_tug_of_war)  
**Submission Repository:** [Suryabhat48/Software_Engineering](https://github.com/Suryabhat48/Software_Engineering)  

---

## 📋 Deliverables Summary

All deliverables specified in the Lab 4 guidelines are organized inside this `Lab-4/` directory:

| Deliverable | Description | File Path |
| :--- | :--- | :--- |
| **a. Videos (Before & After)** | 10-second MP4 video demonstrating the broken deadlock bug before changes | [`videos/gameplay_before.mp4`](videos/gameplay_before.mp4) |
| | 10-second MP4 video demonstrating all four fixed features in action | [`videos/gameplay_after.mp4`](videos/gameplay_after.mp4) |
| **b. Updated Code** | Fully refactored and feature-complete modular Pygame codebase | [`main.py`](main.py), [`game/game_engine.py`](game/game_engine.py), [`game/player.py`](game/player.py), [`game/rope.py`](game/rope.py) |
| **c. Chat History Export** | Complete pair-programming chat history exported as PDF | [`chat_history.pdf`](chat_history.pdf) |
| | Complete pair-programming chat history exported as DOCX | [`chat_history.docx`](chat_history.docx) |

---

## 🛠️ Tasks & Implementation Breakdown

### Task 1: Fix the Alternating Input Deadlock Bug
- **Issue:** Rapid mashing between `A` and `D` froze input handling because the engine relied on `KEYUP` events to clear an `is_pull_locked` flag. During fast human play, overlapping key presses caused `KEYUP` events to fall out of sync, permanently locking out inputs.
- **Fix:** Decoupled pull registration from `KEYUP` lockout. Pulls are verified on `KEYDOWN` by requiring strictly alternating keys (`event.key != self.last_key`). Single-key holding/repeating is ignored while rapid alternating keystrokes register instantaneously without deadlock.

### Task 2: Implement Dynamic AI Panic Surges
- **Feature:** Introduced dynamic AI difficulty scaling based on the rope marker's proximity to the player's winning threshold (`left_win_x`).
- **Mechanics:**
  - When the center flag moves past the midpoint toward the left, `panic_level` increases dynamically from `0.0` to `1.0`.
  - Cadence accelerates: computer pull cooldown drops from `180ms` down to `65ms` (~3x faster reaction rate).
  - Pull strength scales up aggressively up to `+120%` higher pull variance to stage dynamic comebacks.
  - Active visual HUD alert: displays `! AI PANIC SURGE !` with real-time cadence and threat percentage in pulsing amber/red.

### Task 3: Implement Rope Tension & Puller Leaning Animations
- **Puller Leaning Physics (`game/player.py`):**
  - Characters dynamically lean backward based on pulling momentum impulse (`-lean` for Player on left, `+lean` for Computer on right).
  - Smooth spring damping physics interpolates lean angles and relaxes back to rest posture.
  - Pullers stumble slightly forward when violently dragged by the opponent.
  - Renders leaning torso polygons, dynamic head/arm positioning, and strain perspiration particles.
- **Rope Sag & Vibrating Hum Physics (`game/rope.py`):**
  - Models dynamic `struggle_intensity` (0.1 to 1.0).
  - Under low struggle/slack tension: rope exhibits natural downward parabolic sag.
  - Under high struggle/pulling tension: rope becomes taut and exhibits a rapid standing-wave vibrating hum (`math.sin` oscillation).
  - Center flag dynamically tracks the vertical height of the rope curve.

### Task 4: Implement Match Timer & Sudden Death Mode
- **Live Match Timer:** Added real-time timer HUD at the top center of the screen tracking elapsed match duration.
- **Sudden Death Mode:**
  - If a match reaches `45.0` seconds without a winner, **Sudden Death** triggers.
  - Pulling power across all player and computer actions is **doubled (2x multiplier)**, accelerating rope velocity to force a decisive finish.
  - Flashing gold and red HUD banner alerts players: `⚡ SUDDEN DEATH (2X POWER!) ⚡`.

---

## 📜 Separate Git Commit History

Per Instruction 10 (*"Have Separate Commits for each task"*), each milestone was committed individually:

1. `4acd1e8` - **Lab-4: Baseline code and 10s before-fix video demonstrating deadlock bug**
2. `e314203` - **Task 1: Fix alternating input deadlock bug in input synchronization**
3. `67d1c3d` - **Task 2: Implement dynamic AI panic surges with escalating cadence and power**
4. `523b412` - **Task 3: Implement rope tension hum, sag physics, and puller leaning animations**
5. `b090ae4` - **Task 4: Implement live match timer and 45s sudden death mode with 2x pull power**
6. `Final` - **Lab-4: Final deliverables with after-fix video, chat history documentation and README**

---

## 🚀 How to Run the Game

1. Install Pygame (if not already installed):
   ```bash
   pip install pygame
   ```

2. Run the game from this directory:
   ```bash
   python main.py
   ```

3. **Controls:**
   - Rapidly alternate pressing `[A]` and `[D]` to pull left.
   - Press `[R]` to restart after a Game Over.
