import glm
from PIL import Image


class SceneRenderer:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh
        self.scene = app.scene
        # depth buffer
        self.depth_texture = self.mesh.texture.textures['depth_texture']
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)
        # self.cube_fbo = self.ctx.renderbuffer(self.app.WIN_SIZE)
        self.cube_texture = self.mesh.texture.textures['env_cube']
        # self.cube_renderbuffer = self.ctx.renderbuffer(self.app.WIN_SIZE)
        # self.cube_fbo = self.ctx.framebuffer(
        #     color_attachments=[self.ctx.renderbuffer((1600, 1600)) for _ in range(6)])
        self.cube_fbo = [self.ctx.framebuffer(
            color_attachments=[self.ctx.renderbuffer((1000, 1000))]) for _ in range(6)]
        self.cube_angles = (
            (0, 0),  # right
            (180, 0),  # left
            (-90, 90),  # top
            (-90, -90),  # bottom
            (90, 0),  # front
            (-90, 0),  # back
        )
        #
        # self.cube_angles = (
        #     (180, 0),  # right
        #     (0, 0),  # left
        #     (-90, -90),  # top
        #     (-90, 90),  # bottom
        #     (90, 0),  # front
        #     (-90, 0),  # back
        # )

    def render_shadow(self):
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for obj in self.scene.objects:
            obj.render_shadow()

    def render_environment(self):
        if not self.scene.d_reflector:
            return
        else:
            self.app.camera_cube.position = glm.vec3(self.scene.d_reflector.pos)
        # self.app.camera_cube.position = glm.vec3(-1*self.app.camera.position)
        # self.app.camera = self.app.camera_cube
        # self.cube_fbo.use()
        self.app.camera_cube

        for i in range(6):
            self.app.camera_cube.yaw, self.app.camera_cube.pitch = self.cube_angles[i]
            if i in (0, 1, 4, 5):
                flip = True
            else:
                flip = False
            self.app.camera_cube.update(h_flip=flip)
            fbo = self.cube_fbo[i]
            fbo.clear()
            fbo.use()
            self.scene.skybox.render(self.app.camera_cube)
            for obj in self.scene.objects:
                obj.render(self.app.camera_cube)
            self.cube_texture.write(face=i, data=fbo.read(components=3))
        #     data = fbo.read(components=4)
        #     image = Image.frombytes('RGBA', fbo.size, data)
        #     print(f"frame{i}.png")
        #     image.save(f"frame{i}.png")
        # # self.app.camera = self.app.main_cam
        # exit()

    def main_render(self):
        self.app.ctx.screen.use()
        self.scene.skybox.render(self.app.camera)
        for obj in self.scene.objects:
            obj.render(self.app.camera)
        if self.scene.d_reflector:
            self.scene.d_reflector.render(self.app.camera)


    def render(self):
        self.scene.update()
        # pass 1: environment rendering
        self.render_environment()
        # pass 1
        # self.render_shadow()
        # pass 2
        self.main_render()

    def destroy(self):
        self.depth_fbo.release()
        for fbo in self.cube_fbo:
            fbo.release()