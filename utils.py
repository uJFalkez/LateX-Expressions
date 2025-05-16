import streamlit as st
import streamlit.components.v1 as components
import time
import json

def gap(height=8):
    st.markdown(f"""<p style="padding-top:{height}px"> </p>""", unsafe_allow_html=True)

def save_expressions():
    
    with open("expressions.json", 'w', encoding='utf-8') as file:
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
        safe_checked = {k1:{k2:v2 for k2,v2 in v1.items() if isinstance(v2, str)} for k1,v1 in read.items() if isinstance(v1, dict)}
        return safe_checked if safe_checked else None
    except Exception as E:
        print(E)
        return None
    
@st.dialog("Manage Conflicts", width="large")
def conflict_manager(loaded, conflicts):
    st.subheader(f"{len(conflicts)} Conflicting folder{"s" if len(conflicts)-1 else ""}...", anchor=False)
    gap(16)
    for folder in conflicts:
        with st.expander(folder, expanded=True):
            expr_conflicts = st.session_state["saved_expressions"][folder].keys() & loaded[folder].keys()
            if len(expr_conflicts):
                st.subheader(f"{len(expr_conflicts)} Conflicting expression{"s" if len(expr_conflicts)-1 else ""}...", anchor=False)
                gap()
                for expr_name in expr_conflicts:
                    st.write(f"\"{expr_name}\":")
                    col1,col2 = st.columns([1,1])
                    col1.write("Current")
                    col2.write("Uploaded")
                    col1.container(height=100, border=False).latex(st.session_state["saved_expressions"][folder][expr_name])
                    col2.container(height=100, border=False).latex(loaded[folder][expr_name])
            else:
                st.subheader("No expression conflicts.")
            