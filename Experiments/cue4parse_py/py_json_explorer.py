# mostly slop

import json
import sys
import io
import traceback
import dearpygui.dearpygui as dpg
from pprint import pprint

# --- State Management ---
state = {
    "raw_data": {},
    "format_data": {},
    "selected_data": None,
    "selected_path": "None",
    "last_selected_id": None,
    "registry": {},
    "console_history": [],
}


class TooltipStdout(io.StringIO):
    def write(self, s):
        if s.strip():
            msg = s.strip()
            state["console_history"].append(msg)
            if len(state["console_history"]) > 50:
                state["console_history"].pop(0)
            if dpg.does_item_exist("console_output"):
                current_text = dpg.get_value("console_output")
                dpg.set_value("console_output", current_text + msg + "\n")


# --- Debugging ---


def get_extensive_debug():
    try:
        sel_id = state["last_selected_id"]
        info = (
            dpg.get_item_info(sel_id)
            if sel_id and dpg.does_item_exist(sel_id)
            else "None"
        )
        debug_report = {
            "selection": {
                "id": sel_id,
                "type": str(info),
                "path": state["selected_path"],
            },
            "registry_size": len(state["registry"]),
            "data_type": str(type(state["selected_data"])),
        }
        dpg.set_clipboard_text(json.dumps(debug_report, indent=2))
        print("[DEBUG] State copied.")
    except Exception as e:
        print(f"Debug Fail: {e}")


# --- Selection Engine ---


def on_selection(sender, app_data, user_data):
    target_id = user_data
    if not dpg.does_item_exist(target_id):
        return

    last = state.get("last_selected_id")
    new = state.get(target_id)

    if last and dpg.get_item_type(last) == "mvAppItemType::mvSelectable":
        dpg.set_value(last, False)
    # if state["last_selected_id"] and dpg.does_item_exist(state["last_selected_id"]):
    #     dpg.bind_item_theme(state["last_selected_id"], 0)

    with dpg.theme() as sel_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Header, [180, 90, 0, 200])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255])
    dpg.bind_item_theme(target_id, sel_theme)
    state["last_selected_id"] = target_id

    data_slice = state["registry"].get(target_id)
    state["selected_data"] = data_slice
    state["selected_path"] = dpg.get_item_label(target_id)

    render_details_safe(data_slice)


# --- Details Rendering (Explicit Border Flags) ---


def is_compact(d: dict):
    return (
        isinstance(d, dict)
        and len(d) <= 4
        and not any(isinstance(e, dict) for e in d.values())
    )


def render_details_safe(data):
    parent = "details_container"
    dpg.delete_item(parent, children_only=True)

    if data is None:
        dpg.add_text("No Data", parent=parent)
        return

    # Helper to add a table with all borders enabled explicitly
    def add_standard_table(parent_id, header=True):
        return dpg.add_table(
            parent=parent_id,
            header_row=header,
            resizable=True,
            borders_innerH=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_outerV=True,
            policy=dpg.mvTable_SizingFixedFit,
        )

    try:
        # CASE A: List of Dicts
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            dpg.add_text("List of Dicts", parent=parent, color=[100, 200, 255])
            keys = list(data[0].keys())
            t = add_standard_table(parent)
            for k in keys:
                dpg.add_table_column(label=k, parent=t)
            for item in data:
                row = dpg.add_table_row(parent=t)
                for k in keys:
                    dpg.add_text(str(item.get(k, "")), parent=row)

        # CASE B: Dictionary with 1-4 keys (Horizontal Table)
        # elif isinstance(data, dict) and 1 <= len(data) <= 4:
        elif is_compact(data):
            dpg.add_text("Properties (Compact):", parent=parent, color=[100, 200, 255])
            keys = list(data.keys())
            t = add_standard_table(parent)
            for k in keys:
                dpg.add_table_column(label=k, parent=t)
            row = dpg.add_table_row(parent=t)
            for k in keys:
                val = data[k]
                txt = (
                    f"<{type(val).__name__}>"
                    if isinstance(val, (dict, list))
                    else str(val)
                )
                dpg.add_text(txt, parent=row)

        # CASE C: Standard Dictionary or Generic List (Vertical)
        elif isinstance(data, (dict, list)):
            dpg.add_text("Dict or Generic list", parent=parent, color=[100, 200, 255])
            t = add_standard_table(parent)
            dpg.add_table_column(label="Property/Index", parent=t)
            dpg.add_table_column(label="Value", parent=t)
            items = data.items() if isinstance(data, dict) else enumerate(data)
            dicts = []
            for k, v in items:
                row = dpg.add_table_row(parent=t)
                dpg.add_text(str(k), parent=row)
                if isinstance(v, (dict, list)):
                    if is_compact(v):
                        dicts.append(k)

                    dpg.add_text(
                        f"<{type(v).__name__} len:{len(v)}>",
                        parent=row,
                        color=[120, 120, 255],
                    )
                else:
                    dpg.add_text(str(v), parent=row)

            for k, v in items:
                if k not in dicts:
                    continue
                dpg.add_text(k, parent=parent, color=[100, 200, 255])
                ti = add_standard_table(parent)
                for ki, vi in v.items():
                    dpg.add_table_column(label=ki, parent=ti)
                rowi = dpg.add_table_row(parent=ti)
                for ki, vi in v.items():
                    dpg.add_text(str(vi), parent=rowi)

        else:
            dpg.add_text(f"Value: {data}", parent=parent)

    except Exception as e:
        dpg.add_text(f"Render Error: {e}", parent=parent, color=[255, 0, 0])
        traceback.print_exc()


# --- Tree Building ---


def get_node_label(k, v):
    if isinstance(v, dict):
        # name = v.get("Name") or v.get("ObjectName") or str(k)
        name = v.get("Name") or str(k)
        t = v.get("Type") or v.get("Class") or "Object"
        # print(f"{t} - {name}")
        # if t.startswith("{") and t.endswith("}"):
        #     t = "Dict"
        # if t.startswith("[") and t.endswith("]"):
        #     t = "List"
        # if is_named:
        #     return f"{k}| {name} : [{t}]"
        # else:
        return f"{name} : [{t}]"
    return f"{k}: {str(v)[:40]}"


def build_tree_recursive(data, parent_node):
    items = data.items() if isinstance(data, dict) else enumerate(data)
    for k, v in items:
        label = get_node_label(k, v)
        if isinstance(v, (dict, list)) and v:
            item_id = dpg.add_tree_node(
                label=label, parent=parent_node, selectable=False
            )
            build_tree_recursive(v, item_id)
        else:
            item_id = dpg.add_selectable(
                label=label, parent=parent_node, span_columns=True
            )

        state["registry"][item_id] = v
        with dpg.item_handler_registry() as hr:
            dpg.add_item_clicked_handler(callback=on_selection, user_data=item_id)
        dpg.bind_item_handler_registry(item_id, hr)


def load_json(is_format):
    def cb(s, app_data):
        with open(app_data["file_path_name"], "r", encoding="utf-8") as f:
            content = json.load(f)
            if is_format:
                state["format_data"] = content
            else:
                state["raw_data"] = content
        dpg.delete_item("tree_panel", children_only=True)
        state["registry"].clear()
        if not is_format and state["raw_data"]:
            build_tree_recursive(state["raw_data"], "tree_panel")

    return cb


def try_exec(
    source,
    globals,
    locals,
):
    try:
        exec(source, globals, locals)
    except Exception as ex:
        print(ex)


# --- Layout ---
dpg.create_context()
sys.stdout = TooltipStdout()

with dpg.file_dialog(
    show=False, callback=load_json(False), tag="fd_main", width=500, height=400
):
    dpg.add_file_extension(".json")

with dpg.window(label="JSON Explorer", tag="PrimaryWindow"):
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(
                label="Open JSON", callback=lambda: dpg.show_item("fd_main")
            )
            dpg.add_menu_item(label="Copy Debug", callback=get_extensive_debug)

    with dpg.child_window(height=550, resizable_y=True):
        with dpg.group(horizontal=True):
            with dpg.child_window(width=450, resizable_x=True):
                dpg.add_group(tag="tree_panel")
            with dpg.child_window(width=-1):
                dpg.add_group(tag="details_container")

    with dpg.child_window(width=-1, height=-1):
        dpg.add_text("Python Lab", color=[150, 255, 150])
        with dpg.group(horizontal=True):
            dpg.add_input_text(
                tag="code_input",
                multiline=True,
                height=100,
                width=-150,
                default_value="print(f'Path: {selected_path}')",
            )
            dpg.add_button(
                label="EXECUTE",
                width=140,
                height=100,
                callback=lambda: try_exec(
                    dpg.get_value("code_input"),
                    globals(),
                    {
                        "data": state["raw_data"],
                        "selected": state["selected_data"],
                        "selected_path": state["selected_path"],
                    },
                ),
            )
        dpg.add_input_text(
            tag="console_output", multiline=True, readonly=True, height=-1, width=-1
        )

dpg.create_viewport(title="JSON Explorer", width=1400, height=950)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("PrimaryWindow", True)
dpg.start_dearpygui()
dpg.destroy_context()
