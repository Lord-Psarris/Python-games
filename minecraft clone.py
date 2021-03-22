from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as FPS

app = Ursina()

# textures
grass = load_texture('assets/grass_block.png')
dirt = load_texture('assets/dirt_block.png')
stone = load_texture('assets/stone_block.png')
brick = load_texture('assets/brick_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
punch_sound = Audio('assets/assets_punch_sound.wav', loop=False, autoplay=False)

block_pick = 1

window.fps_counter.enabled = False
window.exit_button.visible = False


def update():
    global block_pick
    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',  # u can use a blender texture using '<name of file'>
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            # highlight_color=color.lime,
            scale=0.5
        )

    def input(self, key):
        global block_pick

        if self.hovered:
            if key == 'left mouse down':
                punch_sound.play()
                """normal is the surface of whatever were facing"""
                if block_pick == 1: voxel = Voxel((self.position + mouse.normal), texture=grass)
                if block_pick == 2: voxel = Voxel((self.position + mouse.normal), texture=stone)
                if block_pick == 3: voxel = Voxel((self.position + mouse.normal), texture=brick)
                if block_pick == 4: voxel = Voxel((self.position + mouse.normal), texture=dirt)

            if key == 'right mouse down':
                punch_sound.play()
                destroy(self)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            scale=150,
            double_sided=True,
            texture=sky_texture,
        )


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6)
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)


for z in range(20):
    for x in range(20):
        voxel = Voxel((x, 0, z))

player = FPS()
sky = Sky()
hand = Hand()

app.run()
