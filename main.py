import streamlit as st
from streamlit_scroll_to_top import scroll_to_here
import json
import pyperclip
import random
from utils import *

st.set_page_config(layout="wide", page_title="LaTeX", page_icon=":scroll:")

if st.session_state.get("scroll_to_top", True):
    scroll_to_here(0, key='top')
    st.session_state.scroll_to_top = False
    
for k, v in st.session_state.items():
    if k.startswith("PST."):
        st.session_state[k] = v

if "LISTENER" not in st.session_state:
    st.session_state["LISTENER"] = False
    
if "LISTENER_KEY" not in st.session_state:
    st.session_state["LISTENER_KEY"] = "default"
    
import listener

if "saved_expressions" not in st.session_state or st.session_state.get("reload_expressions", True):
    st.session_state["reload_expressions"] = False
    with open("expressions.json", 'r', encoding='utf-8') as file:
        st.session_state["saved_expressions"] = json.load(file)
    with open("examples.json", 'r', encoding='utf-8') as file:
        st.session_state["example_expressions"] = json.load(file)

if not st.session_state.get("refreshed", 0):
    st.session_state["refreshed"] = 1
    example_name, example_exp = random.choice(list(st.session_state["example_expressions"].items()))
    st.session_state["PST.EXP_NAME_INPUT"] = example_name
    st.session_state["PST.EXP_INPUT"] = example_exp

if st.session_state.get("EXP_INPUT_LOAD", 0):
    st.session_state["PST.EXP_FOLDER_INPUT"], st.session_state["PST.EXP_NAME_INPUT"], st.session_state["PST.EXP_INPUT"] = st.session_state["EXP_INPUT_LOAD"]
    st.session_state["EXP_INPUT_LOAD"] = 0
    st.rerun()

if {} in st.session_state["saved_expressions"].values():
    st.session_state["saved_expressions"] = {k:v for k,v in st.session_state["saved_expressions"].items() if v != {}}
    st.session_state["PST.FOLDER_SELECT"] = None
    st.rerun()
    
if "IMPORT_EXPRESSIONS_FILE_UPLOADER_KEY_CHANGE" not in st.session_state:
    st.session_state["IMPORT_EXPRESSIONS_FILE_UPLOADER_KEY_CHANGE"] = 0

with st.sidebar:
    st.title("Settings")
    st.divider()
    if st.button("Load Example", icon=":material/refresh:", type='primary', use_container_width=True):
        st.session_state["EXP_INPUT_LOAD"] = "", *random.choice(list(st.session_state["example_expressions"].items()))
        st.rerun()
    gap()
    if st.button("Reload Expressions", icon=":material/sync:", type='primary', use_container_width=True):
        st.session_state["reload_expressions"] = True
        st.rerun()
    gap(16)
    
    hide_preview = st.toggle("Hide Expression Preview", value=False)
    gap()
    clear_on_save = st.toggle("Clear on Save", value=False)
    gap()
    lock_delete = st.toggle("Lock delete buttons", value=True)
    gap(16)
    
    font_size = st.number_input("Font-size", value=14, min_value=8, max_value=72)
    gap(32)
    
    st.download_button("Export Expressions",
                       json.dumps(st.session_state["saved_expressions"], indent=4),
                       file_name="expressions.json", type='primary',
                       mime="text/json", icon=":material/download:",
                       help="Select a folder to export" if not st.session_state.get("PST.FOLDER_SELECT", None) else None,
                       use_container_width=True)
    gap(16)
    
    with st.popover("Import Expressions",
                 icon=":material/upload:",
                 use_container_width=True):
        file_import = st.file_uploader("import expressions",
                         key=f"IMPORT_EXPRESSIONS_FILE_UPLOADER_{st.session_state["IMPORT_EXPRESSIONS_FILE_UPLOADER_KEY_CHANGE"]}",
                         type="json",
                         accept_multiple_files=False,
                         label_visibility="hidden")
        if file_import:
            hide_uploader()
            loaded_folders = load_import(file_import)
            valid_import = loaded_folders != None and loaded_folders != {}
            if valid_import:
                folder_count = len(loaded_folders)
                expression_count = len([v1 for v2 in loaded_folders.values() for v1 in v2.values()])
                
                new_folder_count = len(set(loaded_folders) - set(st.session_state["saved_expressions"]))
                new_exprs_count = len([v1 for v2 in {k3:{k4:v4 for k4,v4 in v3.items() if k3 not in st.session_state["saved_expressions"] or k4 not in st.session_state["saved_expressions"][k3]}
                                                     for k3,v3 in loaded_folders.items()}.values() for v1 in v2.values()])
                
                conflicts = {k1:{k2:v2 for k2,v2 in v1.items() if k2 in st.session_state["saved_expressions"][k1] and st.session_state["saved_expressions"][k1][k2] != loaded_folders[k1][k2]}
                             for k1,v1 in loaded_folders.items() if k1 in st.session_state["saved_expressions"] and
                             any([st.session_state["saved_expressions"][k1][k3] != loaded_folders[k1][k3] for k3 in (st.session_state["saved_expressions"][k1].keys() & loaded_folders[k1].keys())])}
                conflict_count = len([v1 for v2 in conflicts.values() for v1 in v2.values()])
                
                divider(1,0,2)
                
                cols = st.columns([1]*(((folder_count+expression_count) > 0) + ((new_folder_count+new_exprs_count) > 0) + (conflict_count > 0)))
                col_counter = 1
                
                with cols[0]:
                    st.write("Found:")
                    st.write(f"- {folder_count} Folder{"s" if folder_count-1 else ""}")
                    st.write(f"- {expression_count} Expression{"s" if expression_count-1 else ""}")
                
                if new_folder_count or new_exprs_count:
                    with cols[1]:
                        st.write("New:")
                        if new_folder_count: st.write(f"- {new_folder_count} Folder{"s" if new_folder_count-1 else ""}")
                        if new_exprs_count: st.write(f"- {new_exprs_count} Expression{"s" if new_exprs_count-1 else ""}")
                        st.write("ㅤㅤㅤㅤㅤㅤㅤㅤㅤ")
                    col_counter += 1
                if len(conflicts):
                    with cols[col_counter]:
                        st.write("Conflicts:")
                        st.write(f"- {len(conflicts)} Folder{"s" if len(conflicts)-1 else ""}")
                        st.write(f"- {conflict_count} Expression{"s" if conflict_count-1 else ""}")
                        st.write("ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ")
                    divider(-1.5)
                    if st.button("Manage conflicts", icon=":material/rule:", use_container_width=True):
                        conflict_manager(loaded_folders, conflicts)
                elif new_folder_count or new_exprs_count:
                    divider(-1.5)
                    if st.button("Commit new expressions", icon=":material/rule:", use_container_width=True):
                        for k, v in loaded_folders.items():
                            if k not in st.session_state["saved_expressions"]:
                                st.session_state["saved_expressions"][k] = v
                            else:
                                st.session_state["saved_expressions"][k].update(v)
                        st.session_state["IMPORT_EXPRESSIONS_FILE_UPLOADER_KEY_CHANGE"] += 1
                        save_expressions()
                        st.rerun()
                else:
                    divider(1,0,2)
                    st.write("No new imports.")
            else:
                st.write("Corrupt file or no expressions found.")

    
    gap(24)
    divider(0,0,3)
    if st.toggle("Listener"):
        gap(24)
        st.session_state["LISTENER_KEY"] = st.sidebar.text_input("Listener socket key", key="PST.LISTENER_KEY", placeholder="default") or "default"
        gap(16)
        st.session_state["LISTENER"] = True
        if st.button("See caught expressions", disabled=not st.session_state["LISTENER"], icon=":material/call_received:", type='primary', use_container_width=True):
            listener_dialog()
    else:
        gap(24)
        with st.popover("What is the Listener?", icon=":material/help:", use_container_width=True):
            st.write("The Listener is a functionality to integrate your test applications with the LaTeX Engine.")
            st.write("It's essentially a socket hosted locally at **/localhost:8501/listener/<key>**")
            st.write("One could send a POST to this socket with LaTeX expressions to be rendered at the app.")
            st.write("For usage examples, refer to <link>, it's not too hard to use.")
        st.session_state["LISTENER"] = False

st.divider()
st.title("LaTeX Expressions Engine", anchor=False)

gap(16)
expr_folder = st.selectbox("Folder:", options=st.session_state["saved_expressions"], placeholder="Folder name", index=None, accept_new_options=True, key="PST.EXP_FOLDER_INPUT")
gap(12)

expr_name = st.text_input("Expression name:", key="PST.EXP_NAME_INPUT")
gap(12)
expr = st.text_area("LaTeX expression:", key="PST.EXP_INPUT", height=200).strip()

if not hide_preview:
    gap(16)
    with st.container(border=True):
        st.container(height=100, border=False).latex(expr)
        if not expr: st.markdown(f"""<p style="margin-bottom:5rem;font-size:{font_size+8}px;text-align:center">Expression preview will be shown here.</p>""", unsafe_allow_html=True)

gap(16)
col1,col2,col3 = st.columns([1,1,1])

if col1.button("Save Expression", icon=":material/save:", type="primary",
               disabled=not expr_folder or not expr_name or not expr, use_container_width=True):
    if expr_folder not in st.session_state["saved_expressions"]:
        st.session_state["saved_expressions"][expr_folder] = {}
    st.session_state["saved_expressions"][expr_folder].update({expr_name:expr})
    save_expressions()
    st.session_state["PST.FOLDER_SELECT"] = expr_folder
    if clear_on_save:
        st.session_state["EXP_INPUT_LOAD"] = "", "", ""
        st.rerun()

if col2.button("Send to New Tab", icon=":material/arrow_outward:",
               disabled=not expr, use_container_width=True):
    load_exp_page(expr_name, expr, font_size)
    
if col3.button("Clear Canvas", icon=":material/delete_sweep:",
               disabled=not expr_folder and not expr_name and not expr, use_container_width=True):
    st.session_state["EXP_INPUT_LOAD"] = "", "", ""
    st.rerun()

if st.session_state["saved_expressions"]:
    st.divider()
    st.header("Saved Expressions", anchor=False)

del_exp = None
gap()
col1,col2 = st.columns([3.95,1])
selected_folder = col1.selectbox("Folder:", placeholder="Select a folder", index=None, key="PST.FOLDER_SELECT", options=st.session_state["saved_expressions"], label_visibility="hidden")
with col2: gap(28)
col2.download_button("Export Folder", json.dumps({selected_folder:st.session_state["saved_expressions"].get(selected_folder, {})}, indent=4),
                     disabled=not selected_folder, type="primary", icon=":material/download:",
                     file_name=f"{selected_folder}_expressions.json",
                     use_container_width=True)

gap(16)

if selected_folder:
    for name, expression in st.session_state["saved_expressions"][selected_folder].items():
        gap()
        col1,col2,col3,col4 = st.columns([12,1,1,1])
        with col1.expander(name):
            with st.container(border=False, height=100):
                st.latex(expression)
            gap(32)
            if st.button("Send to New Tab", key=f"button_print_exp_{name}", type='primary', use_container_width=True):
                load_exp_page(name, expression, font_size)
            
        if col2.button("", icon=":material/content_copy:", key=f"button_copy_expr_{name}", use_container_width=True):
            pyperclip.copy(expression)
            st.toast(f"\"{name}\" was copied to the clipboard!")
            
        if col3.button("", icon=":material/arrow_warm_up:", key=f"button_load_expr_{name}", use_container_width=True):
            st.session_state["EXP_INPUT_LOAD"] = selected_folder, name, expression
            st.session_state.scroll_to_top = True
            st.rerun()
            
        if col4.button("", icon=":material/delete:", key=f"button_delete_expr_{name}", disabled=lock_delete, type="primary", use_container_width=True):
            st.toast(f"\"{name}\" was deleted!")
            del_exp = name

    if del_exp:
        st.session_state["saved_expressions"][selected_folder].pop(name)
        save_expressions()
        st.rerun()
    
st.markdown(f"""<style>
            .katex {{
                font-size: {font_size/10}em
            }}
            .stFileUploader > label {{
                height:0;
                min-height:0;
            }}
            div[class="stVerticalBlock st-emotion-cache-vlxhtx e1lln2w83"] {{
                gap:0;
                }}
            .st-emotion-cache-17o9kmw {{
                display:block;
                overflow-x:auto;
                overflow-y:hidden;
                height:100%;
                
            }}
            </style>""", unsafe_allow_html=True)

with open("teste.json", "r") as file:
    st.download_button("a", file, "teste.json")