from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Load textures
brick_texture = load_texture("brick")  # Ursina has built-in textures
grass_texture = load_texture("grass")
wood_texture = load_texture("white_cube")

# Create player
player = Entity(
    model="cube", color=color.azure, scale=(1, 2, 1), position=(0, 1, 0), collider="box"
)

# Add camera that follows player
camera.parent = player
camera.position = (0, 5, -10)
camera.rotation_x = 20

# Create textured ground
ground = Entity(
    model="plane",
    scale=(20, 1, 20),
    texture=grass_texture,
    texture_scale=(10, 10),
    collider="mesh",
    y=0,
)

# Create walls
walls = []
wall_positions = [
    (0, 2, 10),
    (0, 2, -10),  # Front and back walls
    (10, 2, 0),
    (-10, 2, 0),  # Side walls
]

for pos in wall_positions:
    wall = Entity(
        model="cube",
        scale=(20, 4, 0.5),
        texture=brick_texture,
        texture_scale=(5, 2),
        position=pos,
        collider="box",
        color=color.rgb(255, 255, 255),
    )
    if abs(pos[2]) > 0:  # Rotate front/back walls
        wall.rotation_y = 0
    else:
        wall.rotation_y = 90
    walls.append(wall)

# Add some decorative boxes
for i in range(5):
    box = Entity(
        model="cube",
        scale=(1, 1, 1),
        texture=wood_texture,
        position=(random.randint(-8, 8), 0.5, random.randint(-8, 8)),
        collider="box",
    )

# Add sky
Sky()

# Instructions text
Text(
    text="WASD to move, SPACE to jump, MOUSE to look around",
    scale=1.5,
    origin=(0, -0.5),
    position=(0, 0.4),
)


def update():
    # Player movement
    player.x += held_keys["d"] * 0.1
    player.x -= held_keys["a"] * 0.1
    player.z += held_keys["w"] * 0.1
    player.z -= held_keys["s"] * 0.1

    # Jump
    if held_keys["space"]:
        player.y += 0.2
    if not held_keys["space"]:
        player.y -= 0.1

    # Ground collision
    if player.y < 1:
        player.y = 1


app.run()
