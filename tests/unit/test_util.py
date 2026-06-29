"""Unit tests for util.py — the importable logic of the RDF data converter app."""
import util


# --- markdown_format ---------------------------------------------------------
def test_markdown_format_maps_known_rdf_formats():
    assert util.markdown_format("xml") == "xml"
    assert util.markdown_format("turtle") == "turtle"
    assert util.markdown_format("nt") == "turtle"
    assert util.markdown_format("n3") == "turtle"
    assert util.markdown_format("json-ld") == "json"


def test_markdown_format_returns_empty_for_unknown():
    assert util.markdown_format("does-not-exist") == ""


# --- layout helpers ----------------------------------------------------------
def test_layout_predicates():
    assert util.is_layout_left_right(util.SUPPORTED_LAYOUT_LEFT_RIGHT) is True
    assert util.is_layout_left_right(util.SUPPORTED_LAYOUT_TOP_DOWN) is False
    assert util.is_layout_top_down(util.SUPPORTED_LAYOUT_TOP_DOWN) is True
    assert util.is_layout_top_down(util.SUPPORTED_LAYOUT_LEFT_RIGHT) is False


# --- label_visibility --------------------------------------------------------
def test_label_visibility_all_branches():
    assert util.label_visibility(False, False) == "collapsed"
    assert util.label_visibility(False, True) == "collapsed"
    assert util.label_visibility(True, True) == "collapsed"
    assert util.label_visibility(True, False) == "visible"


# --- read_example_file_to_markdown ------------------------------------------
def test_read_example_file_to_markdown(tmp_path, monkeypatch):
    examples = tmp_path / "examples"
    examples.mkdir()
    (examples / "sample.ttl").write_text("<a> <b> <c> .", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    written = {}

    class _FakeSt:
        def write(self, content):
            written["content"] = content

    util.read_example_file_to_markdown(_FakeSt(), "sample.ttl", "turtle")
    assert "```turtle" in written["content"]
    assert "<a> <b> <c> ." in written["content"]


# --- include_css -------------------------------------------------------------
def test_include_css_concatenates_into_style_tag(tmp_path):
    a = tmp_path / "a.css"
    b = tmp_path / "b.css"
    a.write_text("body{color:red}", encoding="utf-8")
    b.write_text(".x{margin:0}", encoding="utf-8")

    captured = {}

    class _FakeSt:
        def markdown(self, html, unsafe_allow_html=False):
            captured["html"] = html
            captured["unsafe"] = unsafe_allow_html

    util.include_css(_FakeSt(), [str(a), str(b)])
    assert captured["unsafe"] is True
    assert captured["html"].startswith("<style>")
    assert "body{color:red}" in captured["html"]
    assert ".x{margin:0}" in captured["html"]
