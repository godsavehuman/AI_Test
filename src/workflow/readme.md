CodeAgents: A Token-Efficient Framework

This folder contains a small, code-first demonstration of a workflow
runner designed to be easy to unit test and to serve as a scaffold for
LLM-based steps that prioritize token efficiency.

Files added:
- `workflow.py` : minimal Step/Workflow/Runner implementation with example steps.

Design notes
 - Prefer code (callable steps) over large JSON workflows so that prompts,
	 parsing, and state merging can be expressed programmatically and reused.
 - Keep LLM prompts compact: summarize only the active context, use short
	 templates, and avoid repeating unchanged background text across steps.

Pseudocode example (how a real step would use an LLM):

		# Build a concise prompt containing only the small context slice relevant to this step
		prompt = f"Instruction: extract entity. Context: {compact_context_summary}"
		response = llm.call(prompt, max_tokens=128)
		parsed = parse_structured_json(response, schema=...)  # parse safely
		return parsed  # merge into shared context

See `workflow.py` for a runnable Python sample (`sample_workflow`) and tests
in `tests/test_workflow.py` that exercise the runner without performing network calls.






Great — thanks for sharing the article **CodeAgents: A Token‑Efficient Framework for Codified Multi‑Agent Reasoning in LLMs** (arXiv 2507.03254v1). I’ve reviewed it, and below is a structured documentation on how to **construct a workflow for an LLM** in *code-format / pseudocode style*, building off the ideas in the paper. First I’ll summarise the key take-aways, then propose a step-by-step methodology, then show a pseudo-code template you can adapt, and finally a simple example workflow.

---

## 1. Key take-aways from the paper

Here are the main concepts relevant to building workflows in code/pseudocode format:

* The authors argue that rather than prompting LLMs with free-form natural language (which tends to be verbose, ambiguous, and token-inefficient), it’s beneficial to structure workflows as **typed pseudocode with control structures** (loops, conditionals), modular subroutines, typed variables, tool calls, assertions, etc. ([arXiv][1])
* They introduce the notion of roles/agents such as *Planner*, *ToolCaller*, *Replanner/Reviewer* in a multi-agent scheme, though all can live inside one LLM loop. ([arXiv][1])
* They emphasise token-efficiency (reducing input & output tokens) as a design metric. ([arXiv][1])
* They encode tasks as functions in pseudocode, embed assertions (preconditions) and error-feedback loops for replanning. ([arXiv][1])
* The architecture: system prompt sets up tools, roles, cycle ([thought, code, observation]), then the planner outputs pseudocode plan, tool calls are executed, observations come back, if failure then replanner takes over. ([arXiv][1])
* They show empirical gains in benchmarks for accuracy and token usage. ([arXiv][1])

From these points, one can derive a workflow template: define the environment/tools, define roles/agents, write the plan in pseudocode, include execution and feedback loops.

---

## 2. Methodology: How to build a workflow for an LLM

Here is a step-by-step methodology you can apply to construct a workflow in code format for your LLM.

### Step 1: Define the context and tools

* Specify the **task** (what you want the LLM/agent to do).
* List the **available tools** or APIs the agent can call (e.g., search tool, browser tool, database query tool, local computation tool).
* Define what **observations/states** the agent will have access to (e.g., environment state, tool output, intermediate results).
* Define the **roles/agents** if you want modular separation (e.g., Planner, Executor, Reviewer/Replanner).
* Optionally define a **cycle** of operation (e.g., [Thought → Code → Observation] as in the paper).

### Step 2: Write the system prompt in codified format

* Create a structured system prompt (often in YAML or code-like syntax) that sets up the role, tools, cycle, and initial task.
* Example from the paper:

  ```python
  config = 
    role: ‘expert_assistant’
    tools: [GoogleSearchTool, VisitTool, PageUpTool, PageDownTool, FinderTool, TextInspectorTool]
    cycle: [thought, code, observation]
  task = "Search the web and summarize 3 key growth drivers in AI chip market"
  ```

  ([arXiv][1])
* This makes clear what the LLM is supposed to consider, what it can call, and how it should structure its responses.

### Step 3: Plan generation in pseudocode

* Ask the LLM (in Planner role) to generate a high-level plan encoded in pseudocode (e.g., Python-style).
* The plan should include typed variables, function definitions, comments (for human readability), control flow (loops/conditionals) if needed.
* Example structure:

  ```python
  def initial_plan():
      # Step 1: …
      # Step 2: …
      assert precondition_x else: recovery_routine()
      …
  ```

  ([arXiv][1])
* The comments help interpret the logic; the typed variables help enforce structure.

### Step 4: Execution / tool-invocation

* The plan is then “executed” (by the Executor or ToolCaller agent). That means each step corresponds to a tool call or action.
* Example:

  ```python
  query = GoogleSearchTool("…")
  doc = query[0]['url']
  VisitTool(doc)
  …  
  ```

  ([arXiv][1])
* The tool calls may be expressed in JSON or code form depending on your architecture. The paper uses both. ([arXiv][1])

### Step 5: Observation & feedback loop

* After tool calls, you gather observations (tool outputs, environment state).
* The plan can include assertions to check if certain preconditions hold. If an assertion fails, you branch to a recovery path (local) or trigger a replanning loop (global).

  ```python
  assert ’close’ to sofa else: find(’sofa’)
  ```

  ([arXiv][1])
* If failure is serious, you collect error trace (failed instruction, context) and hand to Replanner.

### Step 6: Replanning / revision

* The Replanner uses the error trace to generate an updated plan (again in pseudocode).
* It may reuse parts of the prior plan, adjust steps, branch logic, etc.
* Example:

  ```python
  def updated_plan():
      # Step 3: Ensure near the sofa
      assert ’close’ to ’sofa’ else: find(’sofa’)
      sit(’sofa’)
      eat(’bread’)
  ```

  ([arXiv][1])

### Step 7: Termination / output

* Once the execution completes (no failures or after replanning), you produce final output (result, summary, or action).
* The workflow terminates when the task objective is met.

---

## 3. Pseudocode Template

Here’s a generic template you can adapt for your workflow building:

```python
# SYSTEM PROMPT CONFIGURATION
config = {
    role: 'assistant_agent',
    tools: [ToolA, ToolB, ToolC],
    cycle: ['thought', 'code', 'observation'],
    teammates: [/* optional other agents */]
}
task = "<Describe your task here>"

# PLANNER (generates initial plan)
def initial_plan():
    # Step 1: <description>
    action1 = ToolA(arg1, arg2)
    # Step 2: <description>
    assert <precondition> else: recovery_routine1()
    # Step 3: <description>
    action2 = ToolB(…)
    # …
    return result_variable

# EXECUTOR / TOOLCALLER (executes plan steps)
# (implicitly executed by the agent based on plan above)

# OBSERVATION & FEEDBACK
# For each action, capture:
#   observation = <tool output or state>
#   if <error condition>:
#       error_trace = { 'failed_step': <step>, 'error_message': …, 'context': … }
#       goto REPLANNER

# REPLANNER (if triggered)
def updated_plan(error_trace):
    # Step (resume or revise): <description>
    assert <precondition> else: recovery_routine2()
    action3 = ToolC(…)
    # …
    return result_variable

# TERMINATION
# When result_variable meets success criteria:
final_output = result_variable
```

**Notes and best practices:**

* Use **typed variables** (e.g., `url: String`, `drivers: List[String]`) if your pseudo-code supports that (makes clearer).
* Use **comments** to clarify intent. That helps interpretability and debugging.
* Use **assertions** for preconditions; handle local recovery (e.g., `else: …`) and define when to escalate to a global replanning.
* Use **control flow** (loops, conditionals) if your task requires repetition or branching.
* Separate planning from execution as much as possible — planner produces code, executor runs it, feedback returns to planner/replanner.
* Keep token efficiency in mind: code format tends to be more concise than verbose natural language.
* Maintain modularity: you can define reusable sub-routines/functions for common patterns.
* Collect **error traces** and context to feed into replanner — this supports robustness.
* If you have multiple agents (roles), define clearly which part of the workflow each agent handles.

---

## 4. Example Workflow

Let’s suppose your task is: *“Given a URL list, scrape headlines and summarise the top 3”*. Here’s how you might build a workflow in pseudocode:

```python
# SYSTEM PROMPT CONFIGURATION
config = {
    role: 'web_scraper_agent',
    tools: [WebVisitTool, ExtractTool, SummarizeTool],
    cycle: ['thought', 'code', 'observation']
}
task = "Given the list of URLs, extract the main headline from each and summarise the top 3 headlines."

# PLANNER
def initial_plan(urls: List[String]) -> List[String]:
    headlines: List[String] = []
    for url in urls:
        VisitTool(url=url)
        headline = ExtractTool(keyword="headline")
        assert headline != '' else: continue  # skip if no headline found
        headlines.append(headline)
    # Format: pick top 3 (by order)
    top3 = headlines[:3]
    summary = SummarizeTool(text=top3, focus="main themes", count=1)
    return summary

# EXECUTION & OBSERVATION
# (implicit execution of VisitTool, ExtractTool, SummarizeTool)
# For each iteration, observation = tool output
# If VisitTool fails (e.g., 404), record error_trace:
#    error_trace = {'step': 'VisitTool', 'url': url, 'error': '404'}
#    goto REPLANNER

# REPLANNER
def updated_plan(error_trace, remaining_urls: List[String]) -> List[String]:
    # Remove failed url, continue with next URLs
    filtered_urls = [u for u in remaining_urls if u != error_trace['url']]
    return initial_plan(filtered_urls)

# TERMINATION
final_output = summary
```

You can refine this further (e.g., add retries, fallback extraction logic, more robust filtering) but the skeleton is here.

---

## 5. Documentation Summary

Here is how you might document for your team or for future use:

**Title:** Building Code-Formatted Workflows for LLM Agents
**Purpose:** Provide a structured framework for crafting LLM workflows in pseudocode format that are modular, interpretable, token-efficient, and robust.
**Scope:** Applicable for single-agent or multi-agent workflows where an LLM (or multiple LLM roles) coordinate to perform tasks via tools, observations, and feedback loops.
**Core Concepts:**

* **System Prompt / Configuration:** Define the agent role(s), available tools/APIs, operational cycle, teammates.

* **Planner Agent:** Generates an initial pseudocode plan for the task; uses typed variables, control flow, comments, assertions.

* **Executor / ToolCaller:** Executes the plan’s steps (tool calls); each step produces observation/state.

* **Observation & Feedback Loop:** Assertions verify preconditions; failures produce error traces; decisions to retry locally or escalate globally.

* **Replanner Agent:** Receives error trace and context, revises plan (pseudocode) and executes again.

* **Termination / Output:** The process ends when success criteria are met; final output is returned.
  **Best Practices:**

* Write plans in code-like syntax (“def …(): …”) rather than verbose natural language.

* Use comments for readability but keep overview concise.

* Type annotate variables if possible.

* Embed precondition checks (`assert … else: …`) to build resilience.

* Use loops/conditionals for flexible workflows.

* Separate concerns: planning vs execution vs replanning.

* Keep token cost in mind (especially for large LLMs): compact code representation helps.

* Make parts modular and reusable (e.g., sub-routines).

* Maintain clear error tracking (failed step, context, tool state) to facilitate recovery.
  **Example:** (include the example from section 4)
  **Adaptation Guidelines:**

* For multi-agent settings: define multiple agents in the system prompt (e.g., Planner, ToolCaller, Reviewer) and specify their interactions.

* For tool-rich environments: structure tool invocation clearly and capture tool metadata.

* For dynamic tasks: include loops that check environment state or branching logic based on observations.

* For cost-sensitive tasks: monitor and optimise the number of tokens used by the prompt and outputs; minimise redundancy.

---

If you like, I can **generate a ready-to-use pseudo-code workflow template** (in your choice of language style: Python-like, Javascript-like, etc.) that you can plug your tasks into. Would you like me to produce that?

[1]: https://arxiv.org/html/2507.03254v1 "CodeAgents: A Token-Efficient Framework for Codified Multi-Agent Reasoning in LLMs"




⚙️ 2. Why pseudocode helps reduce overall token cost

Let’s see why structured code workflows are often net more efficient even if they look verbose line-by-line.

a. Compact semantics

Each code construct (like for url in urls: or assert condition) encodes rich, unambiguous meaning in a few tokens.

Compare:

for url in urls:
    VisitTool(url)


vs.

"For each link in the list of URLs, please visit the webpage and extract its content."

The English version requires the model to infer intent every time — which consumes tokens for reasoning, not just text length.

In code, meaning is explicit and structured, so the model doesn’t need to reason “what to do next” repeatedly — it can just execute.


💡 4. Simple example

Plain natural language agent:

Step 1: Go to the website.
Step 2: Search for “AI market.”
Step 3: If you don’t find anything, try again with “AI industry growth.”
Step 4: Summarize the results.

If each failure or replan triggers a new paragraph, total token count balloons quickly.

Code workflow:

query = "AI market"
result = search(query)
if not result:
    query = "AI industry growth"
    result = search(query)
summary = summarize(result)


Even though it looks longer visually, the entire logic can run across multiple cycles without re-prompting.
→ Total tokens for a 4-step process might drop from ~800 to ~250.