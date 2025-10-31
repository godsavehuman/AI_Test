#!/usr/bin/env python3
"""Run pytest for this repo and print a compact JSON summary to stdout.

This script runs `pytest` in a subprocess with `--junitxml` to produce a stable XML
report, parses that XML, and prints a single JSON object describing each test and
an overall summary. The JSON is printed to stdout so an LLM or automation can
consume it directly.

Usage:
    python scripts/llm_test_runner.py

Exit codes:
    0 - script succeeded (tests may still have failures; result JSON will indicate)
    2 - environment error (pytest not installed or other runtime issue)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from typing import Dict, List


def run_pytest_and_emit_xml(xml_path: str) -> int:
    """Run pytest in a subprocess and write JUnit XML to xml_path.

    Returns the subprocess return code.
    """
    cmd = [sys.executable, "-m", "pytest", "--maxfail=1", "-q", "--junitxml", xml_path, "tests"]
    # Run pytest and capture its stdout/stderr so we can print only the JSON later.
    proc = subprocess.run(cmd, capture_output=True, text=True)
    # Optionally, if you want to see pytest output for debugging, uncomment below:
    # print(proc.stdout, file=sys.stderr)
    return proc.returncode


def parse_junit(xml_path: str) -> Dict:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Support both <testsuites> and single <testsuite>
    suites = []
    if root.tag == "testsuites":
        suites = list(root.findall("testsuite"))
    elif root.tag == "testsuite":
        suites = [root]
    else:
        # Unexpected format; still try to find testcases anywhere
        suites = list(root.findall("testsuite"))

    tests: List[Dict] = []
    summary = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0, "time": 0.0}

    for suite in suites:
        # aggregate attributes when present
        try:
            summary["tests"] += int(suite.attrib.get("tests", 0))
            summary["failures"] += int(suite.attrib.get("failures", 0))
            summary["errors"] += int(suite.attrib.get("errors", 0))
            summary["skipped"] += int(suite.attrib.get("skipped", 0))
            summary["time"] += float(suite.attrib.get("time", 0.0))
        except Exception:
            pass

        for tc in suite.findall("testcase"):
            tc_name = tc.attrib.get("name")
            tc_class = tc.attrib.get("classname")
            status = "passed"
            message = None
            for child in list(tc):
                tag = child.tag.lower()
                if tag in ("failure", "error"):
                    status = "failed"
                    message = child.attrib.get("message") or (child.text or "").strip()
                    break
                if tag == "skipped":
                    status = "skipped"
                    message = child.attrib.get("message") or (child.text or "").strip()
                    break

            tests.append({
                "name": tc_name,
                "classname": tc_class,
                "status": status,
                "message": message,
            })

    return {"summary": summary, "tests": tests}


def main() -> int:
    # ensure we have pytest available by attempting to run it; the script below will
    # return an informative JSON error if pytest is missing.
    with tempfile.TemporaryDirectory() as tmpdir:
        xml_path = os.path.join(tmpdir, "results.xml")
        try:
            rc = run_pytest_and_emit_xml(xml_path)
        except FileNotFoundError as e:
            # python or pytest not found
            payload = {"error": "execution_failed", "detail": str(e)}
            print(json.dumps(payload, ensure_ascii=False))
            return 2

        # If the XML wasn't produced, return an error JSON
        if not os.path.exists(xml_path):
            payload = {"error": "no_junit_xml", "pytest_returncode": rc}
            print(json.dumps(payload, ensure_ascii=False))
            return 2

        try:
            result = parse_junit(xml_path)
        except Exception as e:
            payload = {"error": "parse_error", "detail": str(e)}
            print(json.dumps(payload, ensure_ascii=False))
            return 2

        # Print compact JSON to stdout for easy LLM consumption
        print(json.dumps(result, ensure_ascii=False, indent=None))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
