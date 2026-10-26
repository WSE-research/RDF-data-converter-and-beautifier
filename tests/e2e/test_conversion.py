"""End-to-end conversion test: run the app script and convert the bundled examples.

The health-check test only proves that the server starts; Streamlit executes the
app script only when a session connects. This test runs the script with
Streamlit's AppTest, puts each bundled example into the editor (``st_ace``
returns its ``value`` without a browser), selects input and output format, and
checks that the rendered result is the same graph as the input.
"""
from pathlib import Path

import pytest
from rdflib import Graph
from rdflib.compare import isomorphic
from streamlit.testing.v1 import AppTest

REPO_ROOT = Path(__file__).resolve().parents[2]
APP = REPO_ROOT / "rdf_data_converter_and_beautifier.py"
OUTPUT_FORMATS = ("turtle", "json-ld", "xml", "nt", "n3")
# Offline examples only: example2.json loads its @context from schema.org.
EXAMPLES = {
    "turtle": "example1.ttl",
    "xml": "example3.xml",
    "nt": "example5.nt",
    "n3": "example6.n3",
}

pytestmark = pytest.mark.e2e


def _rendered_result(at):
    blocks = [m.value.strip() for m in at.markdown if m.value.strip().startswith("```")]
    assert blocks, "no converted result was rendered"
    lines = blocks[0].splitlines()
    assert lines[-1] == "```"
    return "\n".join(lines[1:-1])


@pytest.mark.parametrize("output_format", OUTPUT_FORMATS)
@pytest.mark.parametrize("input_format", EXAMPLES)
def test_example_is_converted(monkeypatch, input_format, output_format):
    monkeypatch.chdir(REPO_ROOT)  # the app reads images/, css/, js/ and examples/ relative to the cwd
    data = (REPO_ROOT / "examples" / EXAMPLES[input_format]).read_text()

    at = AppTest.from_file(str(APP), default_timeout=60)
    at.session_state["editor"] = data
    at.run()
    assert not at.exception, [e.message for e in at.exception]
    at.selectbox(key="input_format_select").select(input_format)
    at.selectbox(key="output_format_select").select(output_format)
    at.run()

    assert not at.exception, [e.message for e in at.exception]
    assert not at.error, [e.value for e in at.error]
    expected = Graph().parse(data=data, format=input_format)
    converted = Graph().parse(data=_rendered_result(at), format=output_format)
    assert len(converted) == len(expected) > 0
    assert isomorphic(converted, expected)
