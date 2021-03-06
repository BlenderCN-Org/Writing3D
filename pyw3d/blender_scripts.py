# Copyright (C) 2016 William Hicks
#
# This file is part of Writing3D.
#
# Writing3D is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""A collection of scripts to be imported wholesale into Blender
projects"""

MOUSE_LOOK_SCRIPT = """
import bge
import random
import mathutils
def look(cont):
    sensor = cont.sensors["Look"]
    actuator_x = cont.actuators["Look_x"]
    actuator_y = cont.actuators["Look_y"]
    center = (
        bge.render.getWindowWidth()//2,
        bge.render.getWindowHeight()//2)
    if not "look_initialized" in cont.owner:
        cont.owner["look_initialized"] = True
        bge.render.showMouse(not cont.owner["toggle_movement"])
        bge.render.setMousePosition(*center)
    elif cont.owner["toggle_movement"]:
        mouse_pos = sensor.position
        offset = [mouse_pos[i] - center[i] for i in range(2)]

        actuator_y.dRot = [0, 0, -offset[0]*0.001]
        actuator_y.useLocalDRot = False

        actuator_x.dRot = [offset[1]*-0.001, 0, 0]
        actuator_x.useLocalDRot = True

        cont.activate(actuator_x)
        cont.activate(actuator_y)
        bge.render.setMousePosition(*center)

def click(cont):
    camera = cont.owner
    target = camera.worldPosition - camera.getScreenVect(
        *bge.logic.mouse.position
    )
    mouse_click = cont.sensors['Click']
    origin = camera.position
    ray_object = False
    all_ray_objects = set()
    safety = 50
    while ray_object is not None and safety:
        ray_results = camera.rayCast(
            target, origin, {far_clip}, 'clickable', 0, 1
        )
        ray_object = ray_results[0]
        if ray_object:
            del ray_object['clickable']  # Avoid object reselection
            all_ray_objects.add(ray_object)
            if not ray_object['click_through']:
                break  # If no click_through, don't find any more items
        safety += -1

    for ray_object in all_ray_objects:
        ray_object['clickable'] = True
        if mouse_click.positive:
            ray_object['click_status'] = 'selected'
        else:
            ray_object['click_status'] = 'activated'
"""

ANGLES_SCRIPT = """
import mathutils

def target_from_axis(
        axis, angle, initial_orientation=mathutils.Quaternion((1, 0, 0, 0))
    ):
    rotation = mathutils.Quaternion(axis, angle)
    target_orientation = initial_orientation.copy()
    target_orientation.rotate(rotation)
    return target_orientation

def matrix_from_look(look_direction, up_direction):
    rotation_matrix = mathutils.Matrix.Rotation(
        0, 4, (0, 0, 1)
    )
    frame_y = look_direction
    frame_x = frame_y.cross(up_direction)
    frame_z = frame_x.cross(frame_y)
    rotation_matrix = mathutils.Matrix().to_3x3()
    rotation_matrix.col[0] = frame_x
    rotation_matrix.col[1] = frame_y
    rotation_matrix.col[2] = frame_z
    return rotation_matrix

def target_from_look(
        look_point, up_direction, position,
        initial_orientation=mathutils.Quaternion((1, 0, 0, 0))
    ):
    look_direction = (
        mathutils.Vector(position) - mathutils.Vector(look_point)
    )
    up_direction = mathutils.Vector(up_direction).normalized()
    rotation_matrix = matrix_from_look(look_direction, up_direction)
    target_orientation = initial_orientation.copy()
    target_orientation.rotate(rotation_matrix)
    return target_orientation

def target_from_normal(
        normal, angle, initial_orientation=mathutils.Quaternion((1, 0, 0, 0))
    ):
    normal = mathutils.Vector(normal).normalized()
    rotation_matrix = matrix_from_look(
        -normal, mathutils.Vector((0, 0 , 1))
    )
    rotation_matrix = (
        mathutils.Matrix.Rotation(angle, 3, normal) * rotation_matrix
    )
    target_orientation = initial_orientation.copy()
    target_orientation.rotate(rotation_matrix)
    return target_orientation
"""

MOVE_TOGGLE_SCRIPT = """
import bge
import mathutils
def move_toggle(cont):
    toggle_sensor = cont.sensors["toggle_movement"]
    if toggle_sensor.positive:
        cont.owner["toggle_movement"] = not cont.owner["toggle_movement"]
        bge.render.showMouse(not cont.owner["toggle_movement"])
"""

DISABLE_LINK_SCRIPT = """
def disable_link(cont):
    scene = bge.logic.getCurrentScene()
    own = cont.owner
    disabled = cont.sensors['disabled_sensor'].positive
    if disabled:
        try:
            del own['clickable']
        except KeyError:
            pass  # Already unclickable
        disabled_color = {disabled_color}
        for i in range(len(disabled_color)):
            own.color[i] = disabled_color[i]
"""

UNSELECT_LINK_SCRIPT = """
def unselect_link(cont):
    scene = bge.logic.getCurrentScene()
    own = cont.owner
    unselected = cont.sensors['unselected_sensor'].positive
    if unselected:
        own['clickable'] = True
        enabled_color = {enabled_color}
        for i in range(len(enabled_color)):
            own.color[i] = enabled_color[i]
"""

SELECT_LINK_SCRIPT = """
def select_link(cont):
    scene = bge.logic.getCurrentScene()
    own = cont.owner
    selected = cont.sensors['selected_sensor'].positive
    if selected:
        selected_color = {selected_color}
        for i in range(len(selected_color)):
            own.color[i] = selected_color[i]
"""

ACTIVATE_LINK_SCRIPT = """
def activate_link(cont):
    scene = bge.logic.getCurrentScene()
    own = cont.owner
    activated = cont.sensors['activated_sensor'].positive
    remain_enabled = {remain_enabled}
    if activated and own['status'] == 'Stop':
        own['status'] = 'Start'
        own['clicks'] += 1
        if remain_enabled:
            own['click_status'] = 'unselected'
        else:
            own['click_status'] = 'disabled'
"""
