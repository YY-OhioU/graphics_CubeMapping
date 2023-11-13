import glm
import pygame as pg

FOV = 90  # deg
NEAR = 0.1
FAR = 200
SPEED = 0.005
SENSITIVITY = 0.04


class Camera:
    def __init__(self, app, position=(0, 0, 0), yaw=-90, pitch=0, fov=None):
        self.fov = FOV if not fov else fov
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        # view matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()
        self.release_cursor=False

    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))
        # print(self.position, self.yaw, self.pitch)

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        self.move()
        if not self.release_cursor:
            self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_LALT]:
            pg.event.set_grab(False)
            pg.mouse.set_visible(True)
            self.release_cursor = True
        else:
            pg.event.set_grab(True)
            pg.mouse.set_visible(False)
            self.release_cursor = False
        if self.release_cursor:
            return
        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        # if keys[pg.K_q]:
        #     self.position += self.up * velocity
        # if keys[pg.K_e]:
        #     self.position -= self.up * velocity
        if keys[pg.K_SPACE]:
            self.position += self.up * velocity
        if keys[pg.K_LCTRL]:
            self.position -= self.up * velocity

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)


class CameraStatic(Camera):
    def __init__(self, app):
        super().__init__(app, fov=90)

    def update(self, h_flip=False):
        up_vec = glm.vec3(0, 1, 0) if not h_flip else glm.vec3(0, -1, 0)
        # self.move()
        # self.rotate()
        self.update_camera_vectors(up_vec)
        self.m_view = self.get_view_matrix()

    def update_camera_vectors(self, up):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, up))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(self.fov), 1.0, 1, 300)
