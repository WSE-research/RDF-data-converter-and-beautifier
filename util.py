SUPPORTED_LAYOUT_LEFT_RIGHT = "side-by-side"
SUPPORTED_LAYOUT_TOP_DOWN = "editor above formatted code"
SUPPORTED_LAYOUT = (SUPPORTED_LAYOUT_LEFT_RIGHT, SUPPORTED_LAYOUT_TOP_DOWN)

def markdown_format(rdflib_format):
    if rdflib_format == "xml":
        return "xml"
    elif rdflib_format == "turtle":
        return "turtle"
    elif rdflib_format == "nt":
        return "turtle"
    elif rdflib_format == "n3":
        return "turtle"
    elif rdflib_format == "json-ld":
        return "json"
    else:
        return "" # no Markdown formatter known

def is_layout_left_right(layout_format):
    return layout_format == SUPPORTED_LAYOUT_LEFT_RIGHT

def is_layout_top_down(layout_format):
    return layout_format == SUPPORTED_LAYOUT_TOP_DOWN

def label_visibility(agree_on_showing_additional_information, side_by_side_header):
    if not agree_on_showing_additional_information:
        return "collapsed"
    elif side_by_side_header:
        return "collapsed"
    else:
        return "visible"

def read_example_file_to_markdown(st, filename, format):
    with open("examples/" + filename, "r") as f:
        st.write(f"""```{format}\n{f.read()}\n```\n""")

def include_css(st, filenames):
    content = ""
    for filename in filenames:
        with open(filename) as f:
            content += f.read()
    st.markdown(f"<style>{content}</style>", unsafe_allow_html=True)
