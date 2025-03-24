from ursina import *

app = Ursina()


def update():
    if held_keys["a"]:  # Move left when 'a' is held
        player.x -= 1 * time.dt
    if held_keys["d"]:  # Move right when 'd' is held
        player.x += 1 * time.dt


# player = Entity(model="cube", color=color.green)
player = Entity(model="cube", texture="brick")

# Creating 3D environment
ground = Entity(model="plane", texture="grass", scale=(10, 1, 10))

light = DirectionalLight()

camera.position = (0, 5, -10)


app.run()
