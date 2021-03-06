"""
The MIT License (MIT)

Copyright (c) 2013 Niko Skrypnik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
Camera module
=============

In this module different camera classes are implemented. Concept is same as in
THREE.js.
"""


__all__ = ('Camera', )

import math

from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, \
                            AliasProperty
from kivy.graphics.transformation import Matrix
from .math.vectors import Vector3


class Camera(EventDispatcher):
    """
    Base camera class
    """

    scale = NumericProperty(1.0)
    up = ObjectProperty(Vector3(0, 1, 0))

    def __init__(self):
        super(Camera, self).__init__()
        self.projection_matrix = Matrix()
        self.modelview_matrix = Matrix()
        self.renderer = None  # renderer camera is bound to
        self._position = Vector3(0, 0, 0)
        self._position.set_change_cb(self.on_pos_changed)
        self._look_at = None
        self.look_at(Vector3(0, 0, -1))

    def _set_position(self, val):
        if isinstance(val, Vector3):
            self._position = val
        else:
            self._position = Vector3(val)
        self._position.set_change_cb(self.on_pos_changed)

    def _get_position(self):
        return self._position

    position = AliasProperty(_get_position, _set_position)
    pos = position  # just shortcut

    def on_pos_changed(self, coord, v):
        """ Camera position was changed """
        self.look_at(self._look_at)
        self.update()

    def on_up(self, instance, up):
        """ Camera up vector was changed """
        pass

    def on_scale(self, instance, scale):
        """ Handler for change scale parameter event """

    def look_at(self, v):
        m = Matrix()
        pos = self._position * -1
        m = m.translate(pos[0], pos[1], pos[2])
        self.modelview_matrix = m
        self._look_at = v
        self.update()

    def bind_to(self, renderer):
        """ Bind this camera to renderer """
        self.renderer = renderer

    def update(self):
        if self.renderer:
            self.renderer._update_matrices()

    def update_projection_matrix(self):
        """ This function should be overridden in the subclasses
        """


class OrthographicCamera():

    pass


class PerspectiveCamera(Camera):
    """
    Implementation of the perspective camera.
    """

    aspect = NumericProperty()

    def __init__(self, fov, aspect, near, far, **kw):

        super(PerspectiveCamera, self).__init__(**kw)
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far
        self.update_projection_matrix()
        self.bind(aspect=self._on_aspect)

    def _on_aspect(self, inst, value):
        self.update_projection_matrix()
        self.update()

    def update_projection_matrix(self):
        m = Matrix()
        m.perspective(self.fov * 0.5, self.aspect, self.near, self.far)
        self.projection_matrix = m

