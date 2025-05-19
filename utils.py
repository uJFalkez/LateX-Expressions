import streamlit as st
import streamlit.components.v1 as components
import time
import json

FILE_DIR = st.session_state.FILE_DIR

def gap(height=8):
    st.markdown(f"""<p style="padding-top:{height}px"> </p>""", unsafe_allow_html=True)

def divider(top: float = 0, right: float = 0, bottom: float = 0, left: float = 0):
    st.markdown(f"""<hr style="margin:{top}rem {right}rem {bottom}rem {left}rem">""", unsafe_allow_html=True)

def save_expressions():
    
    with open(f"{FILE_DIR}\\expressions.json", 'w', encoding='utf-8') as file:
        json.dump({k:v for k,v in st.session_state["saved_expressions"].items() if v != {}}, file, indent=4)

def load_exp_page(expr_name, expr, font_size):
    safe_expr = expr.replace("\\", "\\\\").replace('"', '\\"')
    nonce = int(time.time() * 1000)

    components.html(f"""
    <script>
        const win = window.open("", "_blank_{nonce}");
        win.document.write(`<!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        background: white;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        font-size: 2.5em;
                    }}
                </style>
                <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"><\\/script>
                <script id="MathJax-script" async
                    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"><\\/script>
            </head>
            <body style='font-size:{font_size+10}px'>
                $$ {safe_expr} $$
            </body>
            </html>`);
        win.document.close();
    </script>
    """, height=0)

def hide_uploader():
    st.markdown("""<style>
            .stFileUploader > section[data-testid="stFileUploaderDropzone"] {
                visibility: hidden;
                height: 0;
                padding: 0;
                }
                </style>""", unsafe_allow_html=True)
    
def load_import(file):
    try:
        read = json.loads(file.read())
        if len(read) == 0: return None
        if not isinstance(list(read.values())[0], dict): return None
        safe_checked = {k1:{k2:v2 for k2,v2 in v1.items() if isinstance(v2, str)} for k1,v1 in read.items() if isinstance(v1, dict) and v1 != {}}
        return safe_checked if safe_checked else None
    except Exception as E:
        print(E)
        return None
    
@st.dialog("Manage Conflicts", width="large")
def conflict_manager(loaded, conflicts):
    save_pos = st.columns([1])[0]
    gap(16)
    st.subheader(f"{len(conflicts)} Conflicting folder{"s" if len(conflicts)-1 else ""}...", anchor=False)
    st.write("(Select to override, don't select to skip)")
    gap(16)
    selection = {}
    for i, folder in enumerate(conflicts.keys()):
        selection.update({folder:{}})
        with st.expander(folder, expanded=True):
            st.subheader(f"{len(conflicts[folder])} Conflicting expression{"s" if len(conflicts[folder])-1 else ""}...", anchor=False)
            divider(1,0,2)
            gap()
            for j, expr_name in enumerate(conflicts[folder].keys()):
                selection[folder].update({expr_name:st.checkbox(f"\"{expr_name}\":", key=f"CHECKBOX-CONFLICT-{j}-{i}")})
                col1,col2 = st.columns([1,1])
                col1.markdown("""<p style="text-align:center">Current</p>""", unsafe_allow_html=True)
                col2.markdown("""<p style="text-align:center">Uploaded</p>""", unsafe_allow_html=True)
                col1.container(key=f"KATEX-CONTAINER-CONFLICT-{j}-{i}-A",height=100, border=False).latex(st.session_state["saved_expressions"][folder][expr_name])
                col2.container(key=f"KATEX-CONTAINER-CONFLICT-{j}-{i}-B", height=100, border=False).latex(conflicts[folder][expr_name])
                divider(1,0,2)
        gap(32)
    
    if save_pos.button("Merge new expressions and override ALL conflicts", icon=":material/warning:", disabled=any([v1 for v2 in selection.values() for v1 in v2.values()]), type="primary", use_container_width=True):
        for k, v in loaded.items():
            st.session_state["saved_expressions"][k].update(v)
        st.session_state["IMPORT_EXPRESSIONS_FILE_UPLOADER_KEY_CHANGE"] += 1
        save_expressions()
        st.rerun()
    
    if st.button("Merge new expressions and override the selected", icon=":material/warning:", disabled=not any([v1 for v2 in selection.values() for v1 in v2.values()]), type="primary", use_container_width=True):
        for k, v in loaded.items():
            if k not in st.session_state["saved_expressions"]:
                st.session_state["saved_expressions"][k] = v
            else:
                st.session_state["saved_expressions"][k].update({k1:v1 for k1,v1 in v.items() if k in selection and k1 in selection[k] and selection[k][k1]})
        st.session_state["IMPORT_EXPRESSIONS_FILE_UPLOADER_KEY_CHANGE"] += 1
        save_expressions()
        st.rerun()
        
@st.dialog("Listener", width="large")
def listener_dialog():
    if not st.session_state["INBOUND_EXPRESSIONS"]:
        st.header("No Expressions Caught!")
    else:
        st.header(f"{len(st.session_state["INBOUND_EXPRESSIONS"])} Expressions Caught!")
        
        st.write(st.session_state["INBOUND_EXPRESSIONS"])
        
        if st.button("Dismiss all", type="primary", use_container_width=True):
            st.session_state["INBOUND_EXPRESSIONS"] = []
            st.rerun()