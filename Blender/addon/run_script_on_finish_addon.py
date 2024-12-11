import bpy
import os
from bpy.app.handlers import persistent

bl_info = {
    "name": "Render Complete Script Executor",
    "description": "Executes a user-defined Python script after render completion",
    "author": "Aaron Hadley",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "category": "Render",
}

class RenderCompleteAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    script_path: bpy.props.StringProperty(
        name="Script Path",
        description="Path to the Python script to execute after render",
        subtype='FILE_PATH'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "script_path")
        layout.operator("render_complete.test_script", text="Test Script")

def execute_user_script(script_path):
    """Execute the user-defined script with arguments."""
    import sys
    if os.path.exists(script_path) and script_path.endswith('.py'):
        try:
            original_argv = sys.argv
            blender_file_name = bpy.path.basename(bpy.data.filepath)
            sys.argv = [script_path, blender_file_name]
            with open(script_path, 'r') as file:
                exec(file.read(), {'__name__': '__main__'})
        except Exception as e:
            print(f"Error executing script: {e}")
        finally:
            sys.argv = original_argv
    else:
        print(f"Invalid script path: {script_path}")

class TEST_OT_RenderCompleteScript(bpy.types.Operator):
    """Test the script execution."""
    bl_idname = "render_complete.test_script"
    bl_label = "Test Script Execution"

    def execute(self, context):
        preferences = bpy.context.preferences.addons[__name__].preferences
        script_path = preferences.script_path
        if script_path:
            print("Testing script execution...")
            execute_user_script(script_path)
        else:
            self.report({'WARNING'}, "No script path specified.")
        return {'FINISHED'}

@persistent
def on_render_complete(scene):
    """Handler that executes after render completion."""
    preferences = bpy.context.preferences.addons[__name__].preferences
    script_path = preferences.script_path
    if script_path:
        print("Render completed. Executing user script...")
        execute_user_script(script_path)

def register_handlers():
    """Ensure the handler is registered and persistent."""
    if on_render_complete not in bpy.app.handlers.render_complete:
        bpy.app.handlers.render_complete.append(on_render_complete)

def unregister_handlers():
    """Remove the handler if it exists."""
    if on_render_complete in bpy.app.handlers.render_complete:
        bpy.app.handlers.render_complete.remove(on_render_complete)

def register():
    """Register add-on classes and handlers."""
    bpy.utils.register_class(RenderCompleteAddonPreferences)
    bpy.utils.register_class(TEST_OT_RenderCompleteScript)
    register_handlers()

def unregister():
    """Unregister add-on classes and handlers."""
    unregister_handlers()
    bpy.utils.unregister_class(TEST_OT_RenderCompleteScript)
    bpy.utils.unregister_class(RenderCompleteAddonPreferences)

if __name__ == "__main__":
    register()
