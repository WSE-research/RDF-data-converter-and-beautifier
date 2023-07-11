import streamlit as st
from streamlit_ace import st_ace
import streamlit.components.v1 as components
from streamlit.components.v1 import html

from rdflib import Graph
from util import SUPPORTED_LAYOUT_LEFT_RIGHT, SUPPORTED_LAYOUT_TOP_DOWN, SUPPORTED_LAYOUT, markdown_format, is_layout_left_right, is_layout_top_down, label_visibility, read_example_file_to_markdown, include_css
from PIL import Image
import base64

import logging

supported_rdf_formats = ("turtle", "json-ld", "xml", "nt", "n3")  # "trig"
EDITOR_KEY = "editor"
RDF_LOGO_SVG = "https://cygri.github.io/rdf-logos/svg/rdf.svg"
PAGE_ICON = "images/rdf_data_converter_and_beautifier.png"
DESCRIPTION = """
This tool enables you to interactively convert RDF data between different formats and beautifies your RDF data. 
Please see our [GitHub repository](https://github.com/WSE-research/RDF-data-converter-and-beautifier/) for more information and how to deploy the tool locally.
                    
You can use the editor to enter RDF data in one of the supported formats (use the select boxes to define your input and output format).
It is also possible to configure the layout of the application in the sidebar. 
There, examples are available as well. 
"""

layout_format = SUPPORTED_LAYOUT_LEFT_RIGHT
input_format = "turtle"
result_format = "json-ld"
side_by_side_header = True
height = 400
agree_on_showing_additional_information = True

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

if EDITOR_KEY not in st.session_state:
    st.session_state[EDITOR_KEY] = ""

st.set_page_config(layout="wide", initial_sidebar_state="expanded",
                   page_title="RDF data converter and beautifier",
                   page_icon=Image.open(PAGE_ICON))

input_head_text = "Original RDF data"
input_label = 'What is the format of the input data?'
input_key = "input_format_select"

result_head_text = "Formatted RDF data"
result_label = 'What is the format of the output data?'
result_key = "output_format_select"


with st.sidebar:
    
    with open("images/rdf_data_converter_and_beautifier.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
        st.sidebar.markdown(
            f"""
            <div style="display:table;margin-top:-20%;margin-bottom:5%;text-align:center">
                <a href="https://github.com/WSE-research/RDF-data-converter-and-beautifier/" title="go to GitHub repository"><img src="data:image/png;base64,{image_data}" style="width:25%;"></a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Configuration")
    agree_on_showing_additional_information = not st.checkbox(
        'minimize layout', value=(not agree_on_showing_additional_information))
    height = st.slider('Height of the editor', 200, 800, value=height, step=25)

    layout_format = st.selectbox(
        'Select layout:', SUPPORTED_LAYOUT, key="layout_format_select")

    include_css(st, ["css/style_streamlit_expander.css",
                "css/style_menu_logo.css", "css/style_github_ribbon.css"])
    st.subheader("Example data")
    st.write("Copy and paste the example data into the editor.")
    with st.expander("Turtle (ttl) example"):
        read_example_file_to_markdown(st, "example1.ttl", "turtle")

    with st.expander("JSON-LD example"):
        read_example_file_to_markdown(st, "example2.json", "json")

    with st.expander("XML example"):
        read_example_file_to_markdown(st, "example3.xml", "xml")

    # with st.expander("TriG example"):
    #    read_example_file_to_markdown(st, "example4.trig", "trig")

    with st.expander("N-Triples (nt) example"):
        read_example_file_to_markdown(st, "example5.nt", "nt")

    with st.expander("N3 example"):
        read_example_file_to_markdown(st, "example6.n3", "n3")

    if not agree_on_showing_additional_information:
        st.markdown("""
""", unsafe_allow_html=True)

# introduce the tool
page_header = """### <img src="{}" style="height:3ex" label="RDF"> data converter and beautifier

{}                    
""".format(RDF_LOGO_SVG, DESCRIPTION)

# show the page header only if the user is not minimizing the layout
if agree_on_showing_additional_information:
    with st.container():
        st.markdown(page_header, unsafe_allow_html=True)
else:
    include_css(st, ["css/remove_space_around_streamlit_body.css"])

# create the layout depending on the user's choice
logging.info("layout: " + str(layout_format))
if layout_format == SUPPORTED_LAYOUT_LEFT_RIGHT:
    side_by_side_header = True
    editor_part_head, result_part_head = st.columns(2)
    editor_part, result_part = st.columns(2)
elif layout_format == SUPPORTED_LAYOUT_TOP_DOWN:
    side_by_side_header = False
    editor_part_head = st.container()
    editor_part = st.container()
    result_part_head = st.container()
    result_part = st.container()
else:
    logging.error("should not happen: layout: " + str(layout_format))


logging.info("input_format: {} => result_format: {}".format(
    input_format, result_format))
index = list(supported_rdf_formats).index(input_format)

# depending on the layout, the header is shown for the format selectors
select_label_visibility = label_visibility(
    agree_on_showing_additional_information, side_by_side_header)

with editor_part:
    input_head_headline_block, input_head_select_block = st.columns([3, 1])
    input_head_description_block = st.container()
    input_index = list(supported_rdf_formats).index(input_format)
    input_head_description = "The editor supports syntax highlighting and code beautification."

    with input_head_headline_block:
        st.subheader(input_head_text)
        if agree_on_showing_additional_information and is_layout_top_down(layout_format):
            st.write(input_head_description)

    with input_head_select_block:
        input_format = st.selectbox(input_label, supported_rdf_formats, key=input_key,
                                    index=input_index, label_visibility=select_label_visibility)

    if agree_on_showing_additional_information and is_layout_left_right(layout_format):
        with input_head_description_block:
            st.write(input_head_description)

    st.session_state[EDITOR_KEY] = st_ace(value=st.session_state[EDITOR_KEY], language=markdown_format(
        input_format), theme="monokai", key="my_code_editor", height=height, auto_update=True)
    logging.debug("content %s: %s", EDITOR_KEY, st.session_state[EDITOR_KEY])

with result_part:
    result_head_headline_block, result_head_select_block = st.columns([
        3, 1])
    result_index = list(supported_rdf_formats).index(result_format)
    result_head_description_block = st.container()
    result_head_description = "The result is formatted using the Markdown code formatter."

    with result_head_headline_block:
        st.subheader(result_head_text)
        if agree_on_showing_additional_information and is_layout_top_down(layout_format):
            st.write(result_head_description)

    with result_head_select_block:
        result_format = st.selectbox(result_label, supported_rdf_formats, key=result_key,
                                     index=result_index, label_visibility=select_label_visibility)

    if agree_on_showing_additional_information and is_layout_left_right(layout_format):
        with result_head_description_block:
            st.write(result_head_description)

    try:
        formatted_code = ""
        if st.session_state[EDITOR_KEY] != "":
            graph = Graph()
            graph.parse(data=st.session_state[EDITOR_KEY], format=input_format)
            result = graph.serialize(format=result_format)
            result_markdown = """ \n```{}\n{}\n```""".format(
                markdown_format(result_format), result)
        else:
            st.warning(
                "Please enter RDF data into the editor or use one of the examples (see sidebar).")
            result_markdown = ""
    except Exception as e:
        result_markdown = ""  # """Error:\n```\n{}\n```""".format(str(e))
        st.error(f"Error while transforming the data given as **{input_format}** format:\n\n{e}")
        st.info(f"Please check the input data **and** the selected input format (currently, *{input_format}* is selected).")

    st.markdown(result_markdown)

st.markdown("""
---
Brought to you by the [<img style="height:3ex;border:0" src="https://avatars.githubusercontent.com/u/120292474?s=96&v=4"> WSE research group](http://wse.technology/) at the [Leipzig University of Applied Sciences](https://www.htwk-leipzig.de/).

See our [GitHub team page](http://wse.technology/) for more projects and tools.
""", unsafe_allow_html=True)

with open("js/change_menu.js", "r") as f:
    javascript = f.read()
    html(f"<script style='display:none'>{javascript}</script>")

html("""
<script>
github_ribbon = parent.window.document.createElement("div");            
github_ribbon.innerHTML = '<a class="github-fork-ribbon right-bottom" href="https://github.com/WSE-research/RDF-data-converter-and-beautifier/" target="_blank" data-ribbon="Fork me on GitHub" title="Fork me on GitHub">Fork me on GitHub</a>';
parent.window.document.body.appendChild(github_ribbon.firstChild);
</script>
""")