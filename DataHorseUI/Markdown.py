import streamlit as st
from streamlit.components.v1 import html
import subprocess
import base64
import os
from fpdf import FPDF

def save_as_pdf(code_cells, text_cells):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for i, code in enumerate(code_cells):
        pdf.multi_cell(0, 10, f"Code Cell {i+1}:\n{code}\n")
    
    for i, text in enumerate(text_cells):
        pdf.multi_cell(0, 10, f"Text Cell {i+1}:\n{text}\n")
    
    pdf_path = "notebook.pdf"
    pdf.output(pdf_path)
    return pdf_path

if "cells" not in st.session_state:
    st.session_state["cells"] = []

def add_cell(cell_type, index=None):
    cell = {"type": cell_type, "content": ""}
    if index is None:
        st.session_state["cells"].append(cell)
    else:
        st.session_state["cells"].insert(index, cell)

def delete_cell(index):
    st.session_state["cells"].pop(index)
    if len(st.session_state["cells"]) == 0:
        del st.session_state["initialized"]

def render_markdown_card(index):
    editor_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
        color: black;
        background-color: white;
        }}
        .editor {{
        border: 1px solid #ccc;
        padding: 10px;
        min-height: 200px;
        color: black;
        background-color: white;
        max-height: 30vh;
        overflow-y: auto;
        }}
        .toolbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        }}
        .toolbar button {{
        margin-right: 5px;
        color: black;
        background-color: #eee;
        border: 1px solid #ccc;
        padding: 5px 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        }}
        .toolbar button:hover {{
        background-color: #ddd;
        }}
        .download-btn {{
        margin-left: auto;
        padding: 5px 10px;
        background-color: #007bff;
        border: none;
        cursor: pointer;
        }}
        .download-btn img {{
        width: 22px;
        height: auto;
        margin-bottom: auto;
        }}
        .markdown-output {{
        border: 1px solid #ccc;
        padding: 10px;
        margin-top: 20px;
        color: black;
        background-color: #D3D3D3;
        white-space: pre-wrap;
        max-height: 30vh;
        overflow-y: auto;
        min-height: 200px;
        }}
    </style>
    <link href="https://cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">
    </head>
    <body>
    <div id="toolbar" class="toolbar">
        <div>
        <button id="bold-button"><b>B</b></button>
        <button id="italic-button"><i>I</i></button>
        </div>
        <button class="download-btn" id="download-button">
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADNklEQVR4AcXUA4wdURiG4VPbtu32mmvUtm3bts2gnNq2bbtBbSzn3n79M8nZrvdcZZO8yUTzPUMGIFmLOlBJTXhtqcPUUaoDxRwp16aObORuHcNpxmwnUjM5/uICam0PyKza2miJSmoGOlH0HlIGjwPUm9tOqrXdD6qt9RANEb39VEGPAXym/5YMK9ehxu5ahKgbH4I3m0rjdoDfBEj+EwDDyrUiiO9UR7ffAd8pMvzHAyJ3Ivr74R7AtD8SIRATURO1ttWBakuCCN4BqrDLAApRiAmAcflm1NilJUSwCAJqqcm8nBs7pRu4y+gCIAoRqdwJ07LtdCfUSSLUlEZqjBQbevwctVvX1QUA7zd8pkYIIfh41o2d0Xh7ICJOpAFOsic0ZHYBIIZQKynjaLQtCPLJVKCrRyQhaAjUYaqIMCBxxA5CqAgRRIjmUMapzBu7oHG0cZmPx2welU4AkARi6T7U3KWHanuAgshCV952hy/sJ1MmNs77Q5mcAHBEuIKwLD6Mmrv1yCS1QMftfsApJjLO+0A1cxjAEb5TwxRE/uX30PmkFrjAgJPRn7lQklMAXwL4TAtB8UVA927PIA8sBNxikC+mhHzMgwA+7j0tFEWXAN1GXkGksSzkMpXxdWBZ/L3LYLvMRBHfqLbCAD7uNT0MJRYDfYedQ4S5FOymonjvbcD7Slb86Fsa9psM9itJIuxUsPhLGG282BJg8ODjgL4QbKbieO+nxyc/NT55a/CughXfu5dLCrGGyir2GcYzPoTGYSiESFNJGtfhk69aSUH4qPG+YoKIc1Q58R+R+Hj8iJ5lYbuUArazKd/QkL9Tv2Lfqb9hpfGiSYzHh3hXxjv05/Di/e23GB8TB/Bxy4xw5YUbMfAwjRdJajw6Yun7KpaM37uWY/YbBDjpIICP023HxH47AV0ehJtLi4wfp0pR7H01M6OvwnGA/9Rf0v/xHTSeF2GWMviQ+PhzykoxJVcA1eZBKh5jvGxi47+oHnzULYCacyFN7is0Po9KRzG3Am7XbzopxFoeoZZyCY0foIrwIbcDZFPxzN+9qy2JZ/whZeADngJEP0k76gB1kOooOuwKIFn7B3LHHIJtp64TAAAAAElFTkSuQmCC" alt="Download">
        </button>
    </div>
    <div id="editor" class="editor"></div>
    <div id="markdown-output" class="markdown-output"></div>
    <script src="https://cdn.quilljs.com/1.3.6/quill.js"></script>
    <script>
        var quill = new Quill('#editor', {{
        modules: {{
            toolbar: '#toolbar'
        }},
        theme: 'snow'
        }});

        document.getElementById('bold-button').addEventListener('click', function() {{
        var range = quill.getSelection();
        if (range) {{
            if (range.length != 0) {{
            var text = quill.getText(range.index, range.length);
            quill.deleteText(range.index, range.length);
            quill.insertText(range.index, '**' + text + '**');
            quill.setSelection(range.index + 2, range.length);
            }}
        }}
        }});

        document.getElementById('italic-button').addEventListener('click', function() {{
        var range = quill.getSelection();
        if (range) {{
            if (range.length != 0) {{
            var text = quill.getText(range.index, range.length);
            quill.deleteText(range.index, range.length);
            quill.insertText(range.index, '*' + text + '*');
            quill.setSelection(range.index + 1, range.length);
            }}
        }}
        }});

        function convertToMarkdown(htmlContent) {{
        return htmlContent
            .replace(/<b>(.*?)<\/b>/g, '**$1**')
            .replace(/<strong>(.*?)<\/strong>/g, '**$1**')
            .replace(/<i>(.*?)<\/i>/g, '*$1*')
            .replace(/<em>(.*?)<\/em>/g, '*$1*')
            .replace(/<br>/g, '\\n\\n')
            .replace(/<[^>]+>/g, '');
        }}

        function markdownParser(text) {{
        return text
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/\\*\\*(.*)\\*\\*/gim, '<b>$1</b>')
            .replace(/\\*(.*)\\*/gim, '<i>$1</i>')
            .trim();
        }}

        document.getElementById('download-button').addEventListener('click', function() {{
        var htmlContent = quill.root.innerHTML;
                var markdownContent = convertToMarkdown(htmlContent);
        var htmlResult = markdownParser(markdownContent);
        document.getElementById('markdown-output').innerHTML = htmlResult;

        // Store the markdown content in a hidden textarea
        document.getElementById('markdown_output_{index}').value = markdownContent;
        }});

        quill.on('text-change', function() {{
        var htmlContent = quill.root.innerHTML;
        var markdownContent = convertToMarkdown(htmlContent);
        document.getElementById('markdown_output_{index}').value = markdownContent;
        }});
    </script>
    <textarea id="markdown_output_{index}" style="display:none;"></textarea>
    </body>
    </html>
    """

    html(editor_html, height=550)

def run_python_code(code):
    try:
        result = subprocess.run(['python3', '-c', code], capture_output=True, text=True, check=True)
        return result.stdout, ""
    except subprocess.CalledProcessError as e:
        return "", e.output

def render_code_card(index, code):
    if "code_outputs" not in st.session_state:
        st.session_state["code_outputs"] = {}
    
    code_input = st.text_area(f"Code Cell {index + 1}:", value=code, height=300, key=f"code_{index}")
    
    output = st.session_state["code_outputs"].get(index, {"output": "", "error": ""})

    if output["error"]:
        st.subheader("Output:")
        st.code("Error: " + output["error"], language='python')
    else:
        st.subheader("Output:")
        st.code(output["output"], language='python')

    if st.button("Run Code", key=f"run_code_{index}"):
        if code_input.strip() == "":
            st.warning("Please enter some Python code.")
        else:
            output_text, error_text = run_python_code(code_input)
            if error_text:
                st.session_state["code_outputs"][index] = {"output": "", "error": error_text}
            else:
                st.session_state["code_outputs"][index] = {"output": output_text, "error": ""}
            st.experimental_rerun()

st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .main-content {
        display: flex;
        flex-direction: column;
        padding: 10px;
        background-color: #2b2b2b;
        border-radius: 5px;
    }
    .add-buttons {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
        margin: 2px;
    }
    .stTextArea textarea, .stCodeCell textarea {
        background-color: #333333;
        color: #ffffff;
        width: 100%;
        height: 200px;
        border: none;
        border-radius: 5px;
        padding: 10px;
    }
    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #1f1f1f;
        padding: 10px;
        border-bottom: 1px solid #444;
    }
    .header img {
        height: 50px;
    }
    .cell {
        max-width: 600px;
        position: relative;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

image_path = "png.png"
image_data = base64.b64encode(open(image_path, "rb").read()).decode() if os.path.isfile(image_path) else "https://via.placeholder.com/200x50"
st.markdown(f'''
    <div class="header">
        <img src="data:image/png;base64,{image_data}" alt="Logo">
        <button onclick="document.getElementById('save-pdf').click()">💾 Save as PDF</button>
    </div>
''', unsafe_allow_html=True)

with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader("Choose files", type=["csv", "xlsx", "txt", "pdf"], accept_multiple_files=True)
    if uploaded_files:
        st.write(f"Uploaded {len(uploaded_files)} file(s)")

st.markdown(
    """
    <style>
    .styled-button {
        background-color: #4CAF50; /* Green */
        border: none;
        color: white;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }
    .styled-button:hover {
        background-color: #45a049;
    }
    .main-content {
        display: flex;
        flex-direction: column;
        padding: 10px;
        background-color: #2b2b2b;
        border-radius: 5px;
    }
    .add-buttons {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
        margin: 2px;
    }
    .stTextArea textarea, .stCodeCell textarea {
        background-color: #333333;
        color: #ffffff;
        width: 100%;
        height: 200px;
        border: none;
        border-radius: 5px;
        padding: 10px;
    }
    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #1f1f1f;
        padding: 10px;
        border-bottom: 1px solid #444;
    }
    .header img {
        height: 50px;
    }
    .cell {
        max-width: 600px;
        position: relative;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
    if "initialized" not in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start Adding Text", key="start_text"):
                st.session_state["initialized"] = True
                add_cell("text")
                st.experimental_rerun()
        with col2:
            if st.button("Start Adding Code", key="start_code"):
                st.session_state["initialized"] = True
                add_cell("code")
                st.experimental_rerun()

    if "initialized" in st.session_state:
        for i, cell in enumerate(st.session_state["cells"]):
            if cell["type"] == "text":
                render_markdown_card(i)
            elif cell["type"] == "code":
                render_code_card(i, cell["content"])

            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            with col1:
                if st.button("Add Text Below", key=f"add_text_{i}"):
                    add_cell("text", i + 1)
                    st.experimental_rerun()
            with col2:
                if st.button("Add Code Below", key=f"add_code_{i}"):
                    add_cell("code", i + 1)
                    st.experimental_rerun()
            with col3:
                if st.button("Delete Cell", key=f"delete_{i}"):
                    delete_cell(i)
                    st.experimental_rerun()

if st.button("💾 Save as PDF"):
    pdf_path = save_as_pdf(st.session_state.code_cells, st.session_state.text_cells)
    st.success(f"Notebook saved as PDF: {pdf_path}")
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
    b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    st.markdown(f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="notebook.pdf" id="save-pdf">Download PDF</a>', unsafe_allow_html=True)