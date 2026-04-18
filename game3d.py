from ursina import (
    Ursina, Entity, Sky, Text, camera, color, window, time, destroy,
    application, held_keys,
)
import random

app = Ursina()

window.title = 'Dino Runner 3D'
window.borderless = False
window.fps_counter.enabled = True
window.exit_button.visible = False

Sky()

LANES = [-3, 0, 3]
GROUND_LENGTH = 40
GROUND_COUNT = 6
GROUND_Y_TOP = 0
PLAYER_SCALE_Y = 2
PLAYER_REST_Y = PLAYER_SCALE_Y / 2
GRAVITY = 45
JUMP_VEL = 16
START_SPEED = 18
MAX_SPEED = 55

ground_segments = []
for i in range(GROUND_COUNT):
    g = Entity(
        model='cube',
        color=color.rgb(170, 130, 80),
        texture='white_cube',
        texture_scale=(4, 8),
        scale=(20, 1, GROUND_LENGTH),
        position=(0, -0.5, i * GROUND_LENGTH),
    )
    ground_segments.append(g)

# Decorative side strips
for side in (-12, 12):
    Entity(
        model='cube',
        color=color.rgb(90, 140, 60),
        scale=(4, 1, GROUND_LENGTH * GROUND_COUNT),
        position=(side, -0.55, GROUND_LENGTH * GROUND_COUNT / 2),
    )

player = Entity(
    model='cube',
    color=color.rgb(110, 110, 110),
    scale=(1, PLAYER_SCALE_Y, 1),
    position=(0, PLAYER_REST_Y, 0),
    collider='box',
)
head = Entity(
    parent=player,
    model='cube',
    color=color.rgb(110, 110, 110),
    scale=(0.9, 0.55, 1.3),
    position=(0, 0.55, 0.3),
)
Entity(parent=head, model='sphere', color=color.white, scale=0.18, position=(-0.22, 0.1, 0.55))
Entity(parent=head, model='sphere', color=color.white, scale=0.18, position=(0.22, 0.1, 0.55))
Entity(parent=head, model='sphere', color=color.black, scale=0.08, position=(-0.22, 0.1, 0.62))
Entity(parent=head, model='sphere', color=color.black, scale=0.08, position=(0.22, 0.1, 0.62))
# Tail
Entity(parent=player, model='cube', color=color.rgb(110, 110, 110),
       scale=(0.4, 0.3, 0.8), position=(0, 0.1, -0.7))

camera.position = (0, 6, -10)
camera.rotation_x = 18
camera.fov = 75

# Clouds
clouds = []
for _ in range(12):
    c = Entity(
        model='sphere',
        color=color.rgb(240, 240, 240),
        scale=(random.uniform(3, 6), 1.5, random.uniform(3, 6)),
        position=(random.uniform(-40, 40), random.uniform(12, 20), random.uniform(20, 200)),
    )
    clouds.append(c)

score_text = Text(text='00000', scale=2, position=(-0.88, 0.46), color=color.black)
hi_text = Text(text='HI 00000', scale=1.3, position=(0.55, 0.46), color=color.rgb(90, 90, 90))
hint_text = Text(
    text='SPACE / UP: jump    A/D or LEFT/RIGHT: change lane    ESC: quit\n\nPress SPACE to start',
    scale=1.1,
    origin=(0, 0),
    position=(0, 0.05),
    color=color.black,
)
over_text = Text(text='', scale=2.5, origin=(0, 0), position=(0, 0.1), color=color.rgb(180, 30, 30))

state = {
    'speed': START_SPEED,
    'score': 0.0,
    'hi': 0,
    'over': False,
    'started': False,
    'lane': 1,
    'vy': 0.0,
    'spawn_timer': 0.0,
}
obstacles = []


def spawn_obstacle():
    lane_x = random.choice(LANES)
    kind = random.random()
    if kind < 0.55:
        obs = Entity(
            model='cube',
            color=color.rgb(50, 140, 60),
            scale=(1, 2, 1),
            position=(lane_x, 1, 70),
            collider='box',
        )
    elif kind < 0.8:
        obs = Entity(
            model='cube',
            color=color.rgb(50, 140, 60),
            scale=(1, 3.2, 1),
            position=(lane_x, 1.6, 70),
            collider='box',
        )
    else:
        obs = Entity(
            model='cube',
            color=color.rgb(50, 140, 60),
            scale=(2.4, 2, 1),
            position=(lane_x, 1, 70),
            collider='box',
        )
    obstacles.append(obs)


def clear_obstacles():
    for o in obstacles:
        destroy(o)
    obstacles.clear()


def reset_game():
    state['speed'] = START_SPEED
    state['score'] = 0.0
    state['over'] = False
    state['started'] = True
    state['lane'] = 1
    state['vy'] = 0.0
    state['spawn_timer'] = 0.0
    player.x = LANES[1]
    player.y = PLAYER_REST_Y
    clear_obstacles()
    hint_text.enabled = False
    over_text.text = ''


def on_game_over():
    state['over'] = True
    state['hi'] = max(state['hi'], int(state['score']))
    hi_text.text = f'HI {state["hi"]:05d}'
    over_text.text = 'GAME OVER\nPress SPACE to restart'


def update():
    if not state['started'] or state['over']:
        return

    dt = time.dt
    state['speed'] = min(START_SPEED + state['score'] * 0.02, MAX_SPEED)

    state['vy'] -= GRAVITY * dt
    player.y += state['vy'] * dt
    if player.y <= PLAYER_REST_Y:
        player.y = PLAYER_REST_Y
        state['vy'] = 0

    target_x = LANES[state['lane']]
    player.x += (target_x - player.x) * min(1, dt * 12)

    state['spawn_timer'] += dt
    spawn_gap = max(0.55, 1.4 - state['score'] * 0.001)
    if state['spawn_timer'] > spawn_gap:
        spawn_obstacle()
        state['spawn_timer'] = 0

    for obs in obstacles[:]:
        obs.z -= state['speed'] * dt
        if obs.z < -10:
            obstacles.remove(obs)
            destroy(obs)
            continue
        if abs(obs.z - player.z) < 1.2 and abs(obs.x - player.x) < 1.1:
            obs_top = obs.y + obs.scale_y / 2
            player_bottom = player.y - PLAYER_SCALE_Y / 2
            if player_bottom < obs_top - 0.1:
                on_game_over()
                return

    for g in ground_segments:
        g.z -= state['speed'] * dt
        if g.z < -GROUND_LENGTH / 2:
            g.z += GROUND_LENGTH * GROUND_COUNT

    for c in clouds:
        c.z -= state['speed'] * 0.3 * dt
        if c.z < -20:
            c.z += 220
            c.x = random.uniform(-40, 40)

    state['score'] += dt * 15
    score_text.text = f'{int(state["score"]):05d}'


def input(key):
    if key == 'escape':
        application.quit()
        return

    if key == 'space' or key == 'up arrow':
        if not state['started'] or state['over']:
            reset_game()
            return
        if player.y <= PLAYER_REST_Y + 0.05:
            state['vy'] = JUMP_VEL

    if not state['started'] or state['over']:
        return

    if key == 'left arrow' or key == 'a':
        state['lane'] = max(0, state['lane'] - 1)
    elif key == 'right arrow' or key == 'd':
        state['lane'] = min(len(LANES) - 1, state['lane'] + 1)


app.run()
