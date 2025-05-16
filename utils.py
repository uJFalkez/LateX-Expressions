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
        return json.loads(file.read())
    except:
        return None