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
st.divider()
st.title("LaTeX Expressions Engine", anchor=False)
    
for k, v in st.session_state.items():
    if k.startswith("PST."):
        st.session_state[k] = v

if "saved_expressions" not in st.session_state:
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

with st.sidebar:
    st.title("Settings")
    st.divider()
    if st.button("Load Example", type='primary', use_container_width=True):
        st.session_state["EXP_INPUT_LOAD"] = "", *random.choice(list(st.session_state["example_expressions"].items()))
        st.rerun()
    gap(16)
    
    hide_preview = st.toggle("Hide Expression Preview", value=False)
    gap()
    transparent_download = st.toggle("Transparent PNG", value=False)
    gap()
    clear_on_save = st.toggle("Clear on Save", value=False)
    gap(16)
    
    font_size = st.number_input("Font-size", value=14, min_value=8, max_value=72)
    gap(32)
    
    st.download_button("Export Expressions",
                       json.dumps(st.session_state["saved_expressions"], indent=4),
                       file_name="expressions.json", type='primary',
                       mime="text/json",
                       icon=":material/download:",
                       use_container_width=True)
    gap(16)
    
    with st.popover("Import Expressions",
                 icon=":material/upload:",
                 use_container_width=True):
        file_import = st.file_uploader("import expressions",
                         type="json",
                         accept_multiple_files=False,
                         label_visibility="hidden")
        if file_import:
            hide_uploader()
            loaded_exprs = load_import(file_import)
            valid_import = loaded_exprs != None and loaded_exprs != {}
            if valid_import:
                conflict_exprs = loaded_exprs.keys() & st.session_state["saved_expressions"]
                gap()
                with st.container(border=True):
                    st.write(f"{len(loaded_exprs)} expression{"s" if len(loaded_exprs)-1 else ""} found!")
                    if len(conflict_exprs):
                        st.write(f"{len(conflict_exprs)} conflicting expression{"s" if len(conflict_exprs)-1 else ""}...")
                        gap()
                        if st.button("Manage conflicts", use_container_width=True):
                            pass
                    gap()
                    if st.button("Commit new expressions", use_container_width=True):
                        pass
            else:
                st.write("Corrupt file or no expressions found.")

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

if col1.button("Save Expression", type="primary", disabled=not expr_folder or not expr_name or not expr, use_container_width=True):
    if expr_folder not in st.session_state["saved_expressions"]:
        st.session_state["saved_expressions"][expr_folder] = {}
    st.session_state["saved_expressions"][expr_folder].update({expr_name:expr})
    save_expressions()
    st.session_state["PST.FOLDER_SELECT"] = expr_folder
    if clear_on_save:
        st.session_state["EXP_INPUT_LOAD"] = "", "", ""
        st.rerun()

if col2.button("Send to New Tab", disabled=not expr, use_container_width=True):
    load_exp_page(expr_name, expr, font_size)
    
if col3.button("Clear Canvas", disabled=not expr_folder and not expr_name and not expr, use_container_width=True):
    st.session_state["EXP_INPUT_LOAD"] = "", ""
    st.rerun()

if st.session_state["saved_expressions"]:
    st.divider()
    st.header("Saved Expressions", anchor=False)

del_exp = None
gap()
selected_folder = st.selectbox("Folder:", placeholder="Select a folder", index=None, key="PST.FOLDER_SELECT", options=st.session_state["saved_expressions"], label_visibility="hidden")
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
            
        if col2.button("Copy", key=f"button_copy_expr_{name}", use_container_width=True):
            pyperclip.copy(expression)
            st.toast(f"\"{name}\" was copied to the clipboard!")
            
        if col3.button("Load", key=f"button_load_expr_{name}", use_container_width=True):
            st.session_state["EXP_INPUT_LOAD"] = selected_folder, name, expression
            st.session_state.scroll_to_top = True
            st.rerun()
            
        if col4.button("Delete", key=f"button_delete_expr_{name}", type="primary", use_container_width=True):
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