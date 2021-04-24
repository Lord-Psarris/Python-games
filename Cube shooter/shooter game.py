from ursina import *
from random import randint
import time
import threading
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

app = Ursina()

window.fps_counter.enabled = False
window.exit_button.visible = False
sky_texture = load_texture('assets/skybox.png')
hits = 0
current_time = 0
to_shoot = True


def count_time():
    global current_time, hits, to_shoot

    while current_time <= 45:
        mins, secs = divmod(current_time, 60)
        mins = round(mins)
        secs = round(secs)
        time_format = '{:02d}-{:02d}'.format(mins, secs)
        text.text = time_format
        time.sleep(1)
        current_time += 1

    Panel(z=1, scale=10, model='quad')
    pane = Text(f'Your score is {hits}', scale=3, origin=(0, 0), background=True)
    pane.create_background(padding=(.5, .25), radius=Text.size / 2)
    to_shoot = False


def spawn(n):
    global enemies
    for i in range(n):
        enemy = Enemy()
        enemy.x = randint(1, 11)
        enemy.z = randint(1, 11)
        enemies.append(enemy)


def update():
    global enemies

    if len(enemies) <= 1:
        spawn(4)


def input(key):
    global to_shoot

    if to_shoot:
        try:
            if key == 'left mouse down':
                b = Bullet((camera.world_position + mouse.normal), camera.forward)
                hand.active()
            else:
                hand.passive()
        except TypeError:
            pass


class Ground(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            model='quad',
            origin_y=0.5,
            color=color.brown,
            position=position,
            rotation=(90, 0, 0),
            texture='brick'
        )


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            scale=150,
            double_sided=True,
            texture=sky_texture,
        )


class Gun(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='cube',
            texture='white_cube',
            scale=(0.2, 0.2, 1),
            color=color.white,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0, -0.6)
        )

    def active(self):
        self.position = Vec2(0, -0.5)

    def passive(self):
        self.position = Vec2(0, -0.6)


class Bullet(Entity):
    def __init__(self, position=(0, 0, 0), direction=None):
        super().__init__(
            model='sphere',
            texture='white_cube',
            scale=0.1,
            color=color.white,
            position=position,
            collider="box",
            direction=direction
        )

    def update(self):
        global hits
        self.position += self.direction
        self.y = 1

        if abs(self.x) > 20:
            self.disable()

        origin = self.world_position + (self.up * .5)  # the ray should start slightly up from the ground so we
        # can walk up slopes or walk over small objects.
        hit_info = raycast(origin, self.direction, ignore=(self,), distance=.5, debug=False)
        if hit_info.hit:
            if hit_info.entity in enemies:
                destroy(hit_info.entity)
                e = enemies.index(hit_info.entity)
                self.disable()
                hits += 1
                hits_text.text = f'{hits} hits'
                enemies.pop(e)


class Enemy(Entity):
    def __init__(self):
        super().__init__(
            parent=scene, model='cube', scale=(1, 2, 1), color=color.lime, texture='white_cube', position=(10, 1, 10),
            collider="box"
        )


for z in range(15):
    for x in range(15):
        ground = Ground((x, 0, z))

text = Text(text='00-00', position=Vec2(0.5, 0.4), color=color.pink, scale=(2, 2, 0))
hits_text = Text(text=f'{hits} hits', position=Vec2(-0.5, 0.4), color=color.pink, scale=(2, 2, 0))

player = FirstPersonController()
hand = Gun()
sky = Sky()
enemies = []
spawn(5)

t = threading.Thread(target=count_time)
t.start()
app.run()
