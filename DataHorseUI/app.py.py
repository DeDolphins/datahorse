import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64
import io
import tempfile
# import markdown2

# Set page configuration
st.set_page_config(
    page_title="DataHorse",
    page_icon="png.png",  # Path to your custom icon file
    layout="wide",
)

# Detect if dark mode is enabled
is_dark_mode = st.get_option("theme.base") == "dark"
logo_path = "png1.png" if is_dark_mode else "png.png"

# Initialize session state
if 'code_cells' not in st.session_state:
    st.session_state.code_cells = [""]

if 'executed_cells' not in st.session_state:
    st.session_state.executed_cells = [None] * len(st.session_state.code_cells)

if 'plots' not in st.session_state:
    st.session_state.plots = [None] * len(st.session_state.code_cells)

# Function to add a new code cell
def add_code_cell():
    st.session_state.code_cells.append("")
    st.session_state.executed_cells.append(None)
    st.session_state.plots.append(None)
    
# # Add Markdown cells
#     pdf.set_font("Arial", 'B', 14)
#     pdf.cell(0, 10, "Markdown Cells", ln=True)
#     pdf.set_font("Arial", size=12)
#     for i, markdown in enumerate(markdown_cells):
#         rendered_text = render_markdown_to_text(markdown)
#         pdf.multi_cell(0, 10, f"Markdown Cell {i+1}:\n{rendered_text}\n")
#         pdf.ln(5)

# Sample dataset for plotting
@st.cache_data
def get_sample_data():
    return pd.DataFrame({
        "Category": ["A", "B", "C", "D"],
        "Values": [23, 45, 12, 30]
    })

sample_data = get_sample_data()

# Function to execute code and generate plot
@st.cache_resource
def generate_plot(code, sample_data):
    fig, ax = plt.subplots()
    if "line" in code:
        ax.plot(sample_data["Category"], sample_data["Values"])
        ax.set_title("Line Plot")
        ax.set_xlabel("Category")
        ax.set_ylabel("Values")
    elif "bar" in code:
        ax.bar(sample_data["Category"], sample_data["Values"])
        ax.set_title("Bar Plot")
        ax.set_xlabel("Category")
        ax.set_ylabel("Values")
    elif "pie" in code:
        ax.pie(sample_data["Values"], labels=sample_data["Category"], autopct='%1.1f%%')
        ax.set_title("Pie Chart")
    else:
        return None
    return fig

# Function to save cells as a PDF with styled comments
def save_as_pdf(code_cells, plots):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Notebook Export", ln=True, align='C')
    pdf.ln(10)

    # Add code cells and plots
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Ask ", ln=True)
    pdf.set_font("Arial", size=12)
    for i, code in enumerate(code_cells):
        code_lines = code.split('\n')
        for line in code_lines:
            if line.strip().startswith("#"):
                pdf.set_text_color(0, 0, 255)  # Blue color for comments
                pdf.multi_cell(0, 10, line)
                pdf.set_text_color(0, 0, 0)  # Reset to black color
            else:
                pdf.multi_cell(0, 10, line)
        pdf.ln(5)

        fig = plots[i]
        if fig:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                fig.savefig(tmpfile.name, format="png")
                pdf.image(tmpfile.name, x=10, y=None, w=180)

    pdf.ln(10)

    # Save the PDF
    pdf_path = "notebook.pdf"
    pdf.output(pdf_path)

    return pdf_path

# Function to process and execute the code in a cell
def process_code_cell(index):
    code = st.session_state.code_cells[index]
    if st.session_state.executed_cells[index] != code:
        st.session_state.executed_cells[index] = code
        st.session_state.plots[index] = generate_plot(code, sample_data)

# Display the Save as PDF button
with st.container():
    st.markdown('<div class="add-buttons">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col5:
        if st.button("💾 Save as PDF"):
            pdf_path = save_as_pdf(st.session_state.code_cells, st.session_state.plots)
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            st.markdown(f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="notebook.pdf" id="save-pdf">Download PDF</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar for file uploads
with st.sidebar:
    st.sidebar.image(logo_path, width=150)
    st.header("Upload Documents")
    uploaded_files = st.file_uploader("")
    if uploaded_files:
        st.write(f"Uploaded {len(uploaded_files)} file(s)")

# Main content area
with st.container():
    for i, code in enumerate(st.session_state.code_cells):
        code_key = f"code_{i}"
        if code_key not in st.session_state:
            st.session_state[code_key] = code

        # Layout for Ask Cell and Icons
        col1, col2, col3 = st.columns([0.9, 0.05, 0.05])
        with col1:
            new_code = st.text_area(
                f"Ask ",
                value=st.session_state[code_key],
                key=code_key,
                height=50,  # Set height
                max_chars=800,
                placeholder="Write your ask here...",
            )
            if new_code != st.session_state.code_cells[i]:
                st.session_state.code_cells[i] = new_code
                process_code_cell(i)

        with col2:
            if st.button(f"▶", key=f"execute_{i}"):
                process_code_cell(i)
        with col3:
            if st.button(f"🗑", key=f"delete_cell_{i}"):
                st.session_state.code_cells.pop(i)
                st.session_state.executed_cells.pop(i)
                st.session_state.plots.pop(i)
                st.experimental_rerun()
        
        # Display output and the "Ask" button after the output
        if st.session_state.plots[i]:
            st.markdown(f"*Output :*")
            st.pyplot(st.session_state.plots[i])
            
            # Add the "Ask" button after the output
            st.markdown('<div class="add-buttons">', unsafe_allow_html=True)
            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                if st.button(f"➕", key=f"add_code_below_{i}"):
                    add_code_cell()
                    st.experimental_rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# Hide MainMenu and Footer
st.markdown(
    """
    <style>
    #MainMenu, footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True
)

st.markdown("""
       <style>
.stTextArea textarea, .stCodeCell textarea {
        background-color: var(--cell-background-light);
        color: var(--text-color-light);
        border: 1px solid #DDDDDD;
        border-radius: 5px;
        padding: 10px;
        font-size: 18px;  /* Increase font size */
        font-family: 'Courier New', Courier, monospace;
        display: flex;
        align-items: center;  /* Vertically center text */
        min-height: 50px;  /* Set a minimum height */
    }
     </style>
# """, unsafe_allow_html=True)

# st.markdown(
#     """
# <style>
# button {
#     height: auto;
#     padding-top: 25px !important;
#     padding-bottom: 25px !important;
# }
# </style>
# """,
#     unsafe_allow_html=True,
# )
# JavaScript to capture Shift+Enter and run the code
# st.markdown("""
#     <script>
#     document.addEventListener("keydown", function(event) {
#         if (event.shiftKey && event.key === "Enter") {
#             event.preventDefault();
#             const codeCells = document.querySelectorAll('.stTextArea textarea');
#             codeCells.forEach((cell, index) => {
#                 if (cell === document.activeElement) {
#                     const executeBtn = document.getElementById(`execute_${index}`);
#                     if (executeBtn) {
#                         executeBtn.click();
#                     }
#                 }
#             });
#         }
#     });
#     </script>
# """, unsafe_allow_html=True)