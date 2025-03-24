from ursina import *

app = Ursina()

# Player
player = Entity(
    model="quad", color=color.red, scale=(0.5, 0.5), position=(-5, -2), collider="box"
)

# Ground and platforms
ground = Entity(
    model="quad", color=color.green, scale=(20, 1), position=(0, -4), collider="box"
)

platforms = [
    Entity(
        model="quad", color=color.brown, scale=(3, 0.5), position=(2, 0), collider="box"
    ),
    Entity(
        model="quad",
        color=color.brown,
        scale=(3, 0.5),
        position=(-3, 2),
        collider="box",
    ),
]

# Physics variables
player.velocity = Vec3(0, 0, 0)
gravity = -9.8
jump_height = 4
can_jump = True


def update():
    global can_jump
    # Horizontal movement
    if held_keys["d"]:
        player.x += 5 * time.dt
    if held_keys["a"]:
        player.x -= 5 * time.dt

    # Apply gravity and update position
    player.velocity.y += gravity * time.dt
    player.y += player.velocity.y * time.dt

    # Check collisions
    hit_info = player.intersects()
    if hit_info.hit:
        if player.velocity.y < 0:  # Only when falling
            if isinstance(hit_info.entity, Entity):  # Ensure valid collision
                player.y = (
                    hit_info.entity.y + hit_info.entity.scale_y / 2 + player.scale_y / 2
                )
                player.velocity.y = 0
                can_jump = True


def input(key):
    global can_jump
    if key == "space":
        if can_jump:
            player.velocity.y = jump_height
            can_jump = False


camera.orthographic = True
camera.fov = 10

app.run()
