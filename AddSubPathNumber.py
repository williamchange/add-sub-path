# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "AddSubPathNumber",
    "author": "None",
    "description": "Increment/Decrement file number from output panel",
    "blender": (2, 83, 0),
    "version": (0, 0, 1),
    "location": "Output Properties > Output",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Render",
}

import bpy, re, os


def process_path(path, increment=True):
    dn = os.path.dirname(path)
    p = os.path.basename(path).rsplit(".", 1)
    if len(re.findall("\d+", p[0])) == 0:
        p[0] += "0"
    s = re.sub("\d+", "{}", p[0])
    nums = [int(n) for n in re.findall("\d+", p[0])]
    try:
        nums[-1] += 1 if increment else -1
        if nums[-1] == 0:
            nums[-1] = -1
    except:
        pass
    path = s.format(*nums)
    if len(p) > 1:
        path += "." + p[1]
    path = path.replace("-1", "")
    return os.path.join(dn, path)


class WM_OT_OUTPATH_INCREMENT(bpy.types.Operator):
    bl_idname = "wm.outpath_increment"
    bl_label = "Add"
    bl_description = "Increment file number"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bpy.app.version >= bl_info["version"]

    def execute(self, context):
        context.scene.render.filepath = process_path(
            context.scene.render.filepath, increment=True
        )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class WM_OT_OUTPATH_DECREMENT(bpy.types.Operator):
    bl_idname = "wm.outpath_decrement"
    bl_label = "Sub"
    bl_description = "Decrement file number"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bpy.app.version >= bl_info["version"]

    def execute(self, context):
        context.scene.render.filepath = process_path(
            context.scene.render.filepath, increment=False
        )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_add_to_render_pt_output(self, context):
    layout = self.layout
    addsub_row = layout.row()
    addsub_row.alignment = "Expand".upper()
    op = addsub_row.operator("wm.outpath_decrement", text="-")
    op = addsub_row.operator("wm.outpath_increment", text="+")


def register():
    bpy.utils.register_class(WM_OT_OUTPATH_INCREMENT)
    bpy.utils.register_class(WM_OT_OUTPATH_DECREMENT)
    bpy.types.RENDER_PT_output.prepend(sna_add_to_render_pt_output)


def unregister():
    bpy.utils.unregister_class(WM_OT_OUTPATH_INCREMENT)
    bpy.utils.unregister_class(WM_OT_OUTPATH_DECREMENT)
    bpy.types.RENDER_PT_output.remove(sna_add_to_render_pt_output)
