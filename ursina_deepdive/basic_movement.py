from ursina import *

app = Ursina()

# Create a player
player = Entity(model="cube", color=color.red, scale_y=2, position=(0, 1, 0))

# Create ground
ground = Entity(model="plane", scale=(100, 1, 100), color=color.green, collider="box")


# Add gravity
def update():
    player.y += held_keys["space"] * 1
    player.y -= 0.5
    if player.y < 1:
        player.y = 1

    player.x += held_keys["d"] * 0.5
    player.x -= held_keys["a"] * 0.5
    player.z += held_keys["w"] * 0.5
    player.z -= held_keys["s"] * 0.5


# Add camera that follows player
camera.parent = player
camera.position = (0, 2, -8)
camera.rotation = (10, 0, 0)

# Add sky
Sky()

# Add instructions text
Text(text="WASD to move, Space to jump", scale=2, origin=(0, 0))

app.run()
