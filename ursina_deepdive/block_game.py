from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()


# Game state
class GameState:
    def __init__(self):
        self.score = 0
        self.blocks_placed = 0
        self.target_height = 5
        self.game_won = False


game_state = GameState()

# UI
score_text = Text(text=f"Score: {game_state.score}", position=(-0.85, 0.45))
height_text = Text(
    text=f"Target Height: {game_state.target_height}", position=(-0.85, 0.4)
)
game_message = Text(
    text="Build a tower to reach the target height!", position=(0, 0.35)
)


class Voxel(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model="cube",
            origin_y=0.5,
            texture="white_cube",
            color=color.hsv(random.random(), 0.7, 0.9),
            highlight_color=color.lime,
            collider="box",
        )
        self.velocity = Vec3(0, 0, 0)
        self.gravity = 9.8
        self.is_static = position[1] == 0
        self.height = position[1]

    def check_support(self):
        if self.y <= 0:
            return True
        hit_info = raycast(
            self.position + Vec3(0, 0.1, 0), Vec3(0, -1, 0), distance=1.1, ignore=[self]
        )
        return hit_info.hit and isinstance(hit_info.entity, Voxel)

    def update(self):
        if self.is_static and not self.check_support():
            self.is_static = False
            self.velocity = Vec3(0, 0, 0)

        if not self.is_static:
            self.velocity.y -= self.gravity * time.dt
            hit_info = raycast(
                self.position + Vec3(0, 0.1, 0),
                Vec3(0, -1, 0),
                distance=1.1,
                ignore=[self],
            )

            if hit_info.hit and isinstance(hit_info.entity, Voxel):
                self.y = hit_info.entity.y + 1
                self.velocity.y = 0
                if abs(self.velocity.y) < 0.1:
                    self.is_static = True
                    # Check if this block helps reach the target height
                    if (
                        int(self.y) >= game_state.target_height
                        and not game_state.game_won
                    ):
                        game_state.game_won = True
                        game_state.score += 100
                        game_state.target_height += 2
                        game_message.text = "Level Complete! New target height set!"
                        score_text.text = f"Score: {game_state.score}"
                        height_text.text = f"Target Height: {game_state.target_height}"
            else:
                self.position += self.velocity * time.dt


# Create ground platform
platform_size = 20
for z in range(-platform_size // 2, platform_size // 2):
    for x in range(-platform_size // 2, platform_size // 2):
        voxel = Voxel(position=(x, -1, z))

# Create initial spawn platform
spawn_size = 3
for z in range(-spawn_size, spawn_size + 1):
    for x in range(-spawn_size, spawn_size + 1):
        voxel = Voxel(position=(x, 0, z))


def input(key):
    if key == "escape":
        application.quit()
    if key == "left mouse down":
        hit_info = raycast(
            camera.world_position, camera.forward, distance=5, ignore=[player]
        )
        if hit_info.hit:
            new_position = hit_info.entity.position + hit_info.normal
            existing = raycast(new_position, Vec3(0, 0, 0), distance=0.1)
            if not existing.hit:
                Voxel(position=new_position)
                game_state.blocks_placed += 1
                game_state.score += 1
                score_text.text = f"Score: {game_state.score}"

    if key == "right mouse down" and mouse.hovered_entity:
        if isinstance(mouse.hovered_entity, Voxel):
            pos = mouse.hovered_entity.position
            above = raycast(pos + Vec3(0, 1, 0), Vec3(0, 1, 0), distance=1)
            if above.hit and isinstance(above.entity, Voxel):
                above.entity.is_static = False
            destroy(mouse.hovered_entity)
            game_state.score -= 1
            score_text.text = f"Score: {game_state.score}"


player = FirstPersonController(position=(0, 1, 0))
player.gravity = 9.8
player.jump_height = 2
player.jump_duration = 0.5
player.air_time = 0
player.velocity_y = 0
player.is_grounded = False
player.jump_cooldown = 0


def update():
    hit_info = raycast(
        player.position + Vec3(0, 0.1, 0), Vec3(0, -1, 0), distance=1.1, ignore=[player]
    )

    if player.jump_cooldown > 0:
        player.jump_cooldown -= time.dt

    if hit_info.hit:
        player.is_grounded = True
        player.y = hit_info.point.y + 1
        player.air_time = 0
        if player.velocity_y < 0:
            player.velocity_y = 0
    else:
        player.is_grounded = False
        player.air_time += time.dt
        player.velocity_y -= player.gravity * time.dt

    if held_keys["space"] and player.is_grounded and player.jump_cooldown <= 0:
        player.velocity_y = sqrt(2 * player.gravity * player.jump_height)
        player.jump_cooldown = 0.2
        player.is_grounded = False

    player.y += player.velocity_y * time.dt


Sky()
app.run()
