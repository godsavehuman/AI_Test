# AI_Test - local file DB test project

This repository contains a minimal Python module that implements a small local file-based key-value store and unit tests to validate it.

Files created:

- `src/local_db.py` - LocalFileDB implementation (JSON files per key).
- `tests/test_local_db.py` - pytest unit tests covering save/get/delete and key sanitization.
- `requirements.txt` - test dependencies (pytest)

How to run tests (PowerShell on Windows):

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
```

LLM / automation: run tests and produce machine-readable output

If you want an LLM or automation to both run and read the test results, produce a machine-readable report (JUnit XML) that can be parsed programmatically. From PowerShell run:

```powershell
# run all tests and write JUnit XML to results.xml (recommended for tooling/LLMs)
python -m pytest --maxfail=1 -q --junitxml=results.xml

# show the XML report content so a reader/agent can parse it
Get-Content results.xml -Raw
```

To run only the single test module in this repo and produce the same XML report:

```powershell
python -m pytest tests/test_local_db.py --maxfail=1 -q --junitxml=results.xml
Get-Content results.xml -Raw
```

Notes and optional tooling:
- `--junitxml` is built into pytest and requires no extra plugins; XML is well-suited for programmatic parsing.
- If you prefer JSON output, you can install a plugin such as `pytest-json-report` and run `pytest --json-report --json-report-file=results.json` (not included in `requirements.txt` by default).

Notes:
- The DB stores one JSON file per key under the provided data directory.
- Keys are preserved in the file payload so `list_keys()` returns original keys.

Next steps you might try:
- Add a small CLI or REST API wrapper around the DB.
- Add concurrency tests or file-locking for multi-process safety.


knowledge base
look through to find past experience 

workflow 



skill(tool) tree (tool)
select skills based on knowledge




cypher
CREATE (r:Root {name: 'Tool Directory'})
CREATE (c1:Category {name: 'Hand Tools'})
CREATE (c2:Category {name: 'Power Tools'})
CREATE (c3:Category {name: 'Cutting'})
CREATE (c4:Category {name: 'Driving'})

CREATE (r)-[:HAS_CATEGORY]->(c1)
CREATE (r)-[:HAS_CATEGORY]->(c2)
CREATE (c1)-[:HAS_SUBCATEGORY]->(c3)
CREATE (c1)-[:HAS_SUBCATEGORY]->(c4);
Use code with caution.

B. Create the Tool Nodes and Link Them:
cypher
CREATE (t1:Tool {name: 'Saw', description: 'Used for cutting wood'})
CREATE (t2:Tool {name: 'Hammer', description: 'Used for driving nails'})
CREATE (t3:Tool {name: 'Drill', description: 'Used for making holes'})

MATCH (c:Category {name: 'Cutting'}) CREATE (t1)-[:IN_CATEGORY]->(c)
MATCH (c:Category {name: 'Driving'}) CREATE (t2)-[:IN_CATEGORY]->(c)
MATCH (c:Category {name: 'Power Tools'}) CREATE (t3)-[:IN_CATEGORY]->(c);
Use code with caution.

3. Querying Data Efficiently
Graph databases excel at traversing these relationships. The queries below leverage index-free adjacency for speed, as the database follows direct pointers rather than performing slow table joins.
A. Find all tools within a specific category (and its subcategories):
This query uses a variable-length path (*.. notation) to traverse any depth of subcategories until it finds a tool.
cypher
MATCH (target:Category {name: 'Hand Tools'})-[:HAS_SUBCATEGORY*0..]->(sub:Category)<-[:IN_CATEGORY]-(tool:Tool)
RETURN tool.name AS ToolName, sub.name AS Category
Use code with caution.

Note: *0.. ensures the target category itself is included in the search depth.
B. Find the complete hierarchical path for a single tool:
This query is efficient because it starts at the tool node and traverses up the hierarchy to the root.
cypher
MATCH path = (t:Tool {name: 'Saw'})<-[:IN_CATEGORY]-(c:Category)<-[:HAS_SUBCATEGORY*]-(root:Root)
RETURN nodes(path)
Use code with caution.

C. Find all tools in the entire directory:
cypher
MATCH (r:Root)-[:HAS_CATEGORY*]->(c:Category)<-[:IN_CATEGORY]-(t:Tool)
RETURN t.name
