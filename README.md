# Card guide

One CrewAI agent answers a question from the Markdown model cards in `cards/`. It runs on a local model through [Ollama](https://ollama.com). No cloud API key is required.

The crew is sequential, with a single agent and a single task. The agent searches the cards, reads one file, then answers. A checker looks at the answer before it is accepted. Identical tool calls in the same run are reused from memory.

```text
cards/                         # the model cards the agent may read
starter/
  setup.py                     # starts Ollama and downloads the model
  main.py                      # what you run
  llm.py                       # the only place the model is chosen
  crew.py                      # wires the agent, task, tools, and cache
  settings.py                  # reads starter/config/settings.yaml
  config/agents.yaml           # the card-guide role
  config/tasks.yaml            # the answer step
  config/settings.yaml         # how many search hits to return
  tools/search_cards.py        # find cards by words in the question
  tools/read_card.py           # open one card by filename
  guardrail/answer_check.py    # reject an answer that is not grounded
```

`{question}` in the YAML files is filled in when you run the crew.

## What you need

- Python 3.10, 3.11, 3.12, or 3.13
- About 8 GB of free disk for `qwen2.5:7b`
- [Ollama](https://ollama.com) installed and able to reach `http://localhost:11434`

`qwen2.5:7b` is the model this project uses. It calls `search_cards` and `read_card`. `llama3.1:8b` often writes a fake tool call as plain text and invents a card, so leave it off for this demo.

## 1. Install Ollama

**macOS:** download the app from [ollama.com](https://ollama.com), or:

```bash
brew install ollama
```

**Linux:**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:** download the installer from [ollama.com](https://ollama.com).

You only need the Ollama program installed in this step. The next step starts it and downloads the model. Do not run `ollama pull` yourself: if your shell has `OLLAMA_HOST` pointed at a port where nothing is listening, that command fails even when Ollama is already running.

## 2. Set up this project

From the project folder, check the Python version first. It must be 3.10 or newer. Python 3.8 and 3.9 cannot install current CrewAI.

```bash
python3 --version
python3 -m venv .venv
```

If that `python3` is too old, install Python 3.12 and create the environment with it, for example `python3.12 -m venv .venv`.

Activate the virtual environment:

```bash
# macOS and Linux
source .venv/bin/activate

# Windows Command Prompt
.venv\Scripts\activate.bat

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies with the virtual environment's Python, not the system `pip`:

```bash
python -m pip install -r requirements.txt
```

`python` here must be 3.10 or newer. If this `.venv` was created with uv, it has no `pip` module. Use uv instead:

```bash
uv pip install --python .venv/bin/python -r requirements.txt
```

A bare `pip` can be `/usr/bin/pip` even when `(.venv)` is showing. That pip is often Python 3.8, and it only sees CrewAI 0.1.x, so the install fails on `crewai[litellm]>=1.2.0`.

Copy the environment file and set the model this project expects:

```bash
cp .env.example .env
```

On Windows Command Prompt use `copy .env.example .env`.

In `.env`, set:

```bash
OLLAMA_MODEL=qwen2.5:7b
```

Start Ollama if it is stopped, and download that model:

```bash
python -m starter.setup
```

This looks for a server on `http://127.0.0.1:11434` and on `OLLAMA_HOST`. If one is already running, the download uses that server. If none is running, it starts Ollama on port `11434` and downloads there. A stale `OLLAMA_HOST` in `~/.bashrc` cannot send the download to the wrong port.

The first download is several gigabytes. When the command prints `Ready`, continue to the next step. The first search also downloads the NLTK English stopword list.

## 3. Run it

```bash
python -m starter.main
```

With no argument, the question is `What license does bert-base-uncased use?`. The answer should name `bert-base-uncased.md` and Apache License 2.0.

Pass your own question as an argument. It replaces `{question}` in the agent and task files:

```bash
python -m starter.main "What license does bert-base-uncased use?"
```

To change the default without passing an argument, set `QUESTION` in `.env`. If that variable is missing, the BERT license question above is used.

The first run is slow because the model loads into memory.

## What the agent does

1. `search_cards` scores each file in `cards/` by how often the question's words appear. English stopwords and words of two letters or fewer are dropped. It returns up to `search.max_hits` filenames and a short snippet. That limit is `8` in `starter/config/settings.yaml`.
2. `read_card` opens one `.md` file by name. Paths outside `cards/` are refused.
3. The agent writes a short answer and names the file, or says the collection does not contain the answer.

`max_iter: 8` in `starter/config/agents.yaml` is how many think-and-tool steps one attempt may take. `cache=True` in `starter/crew.py` keeps tool results in memory for this run only. A second call with the same tool and the same arguments does not read the file again. The cache is gone when the program exits.

## The answer checker

`starter/guardrail/answer_check.py` runs after the agent finishes, not during the tool steps. `guardrail_max_retries: 3` in `starter/config/tasks.yaml` means the first answer plus up to three more tries. Those retries are separate from `max_iter`.

The checker accepts an answer that names a real file in `cards/` and does not paste lines or a license that the file does not contain. It also accepts a clear "the collection does not contain the answer" when no card text is pasted. It rejects a missing filename, a filename that is not in the folder, pasted lines that are not in the named file, and a license phrase that is not in that file.

A grounded filename with a wrong sentence can still pass if that sentence is not pasted card text and not a recognized wrong license. The checker does not prove the whole answer is correct.

## 4. Point it at a different model

Edit `.env`:

```bash
OLLAMA_MODEL=qwen2.5:7b
```

Download that model with the same setup command. It reads `OLLAMA_MODEL` from `.env`:

```bash
python -m starter.setup
```

Keep `LLM_TEMPERATURE` around `0.2`.

If Ollama runs on another computer, set the host and start Ollama so it listens on the network:

```bash
OLLAMA_BASE_URL=http://192.168.1.20:11434
```

On the Ollama machine:

```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

## 5. Use LM Studio or another local server

Any server that speaks the OpenAI chat API works. In LM Studio, start the local server (default `http://localhost:1234`). Then set `.env` like this:

```bash
LLM_PROVIDER=openai_compatible
OPENAI_API_BASE=http://localhost:1234/v1
OPENAI_MODEL_NAME=your-model-name-as-shown-in-lm-studio
OPENAI_API_KEY=lm-studio
```

`starter/llm.py` reads those values. You do not need to change the agent. The model still has to be willing to call tools.

## 6. Add an agent

1. Add a block to `starter/config/agents.yaml`. The top-level name is the method name you will add in Python. Set `llm: local` so it uses the same model.

```yaml
editor:
  role: Editor
  goal: Tighten the answer to {question} without adding new claims
  backstory: You cut repetition and flag anything the card does not support.
  llm: local
  verbose: true
  max_iter: 5
```

2. Add a method in `starter/crew.py` with the same name:

```python
@agent
def editor(self) -> Agent:
    return Agent(config=self.agents_config["editor"])
```

3. Give that agent a task (next section). An agent with no task does not run.

## 7. Add a task

1. Add a block to `starter/config/tasks.yaml`. `agent` must match an `@agent` method. `context` lists earlier tasks whose output this step should see.

```yaml
edit_answer:
  description: Edit the answer to {question}. Keep every claim tied to the card.
  expected_output: The revised answer, plus a short list of cuts you made.
  agent: editor
  context:
    - answer_question
```

2. Add the matching method in `starter/crew.py`:

```python
@task
def edit_answer(self) -> Task:
    return Task(config=self.tasks_config["edit_answer"])
```

Tasks run in the order they are declared in `tasks.yaml`.

## 8. Add a tool

`search_cards` and `read_card` are already wired. To add another tool, copy `starter/tools/example_tool.py`, change the class, then expose it from the crew:

```python
@tool
def my_tool(self):
    return MyTool()
```

Reference `my_tool` under `tools:` in the agent YAML. The YAML name and the method name must match.

`starter/tools/example_tool.py` is only a pattern. It is not used by the card guide.

## If it fails

| What you see | What to do |
| --- | --- |
| `could not connect to ollama server` after `ollama pull` | Run `python -m starter.setup` instead. Your shell's `OLLAMA_HOST` is pointed at a different port than the running server. |
| `Ollama is not running` | Run `python -m starter.setup`. It starts the server on port 11434. |
| Model is not installed | Run `python -m starter.setup`, or set `OLLAMA_MODEL` in `.env` to a model you already have and run setup again. |
| The answer invents a card and never calls a tool | Set `OLLAMA_MODEL=qwen2.5:7b` and run `python -m starter.setup`. |
| The checker rejects the answer | Read the retry note. The answer must name a real file in `cards/`, or say the collection does not contain the answer. |
| `OPENAI_API_KEY` error | Copy `.env.example` to `.env`. The Ollama path does not call OpenAI; CrewAI still wants a placeholder key when you switch providers. |
| Connection error to another machine | Use that machine's real IP in `OLLAMA_BASE_URL`, and start Ollama with `OLLAMA_HOST=0.0.0.0:11434`. |

## Project layout

| File | Role |
| --- | --- |
| `cards/` | Model cards the agent is allowed to read |
| `starter/setup.py` | Starts Ollama and downloads the model in `.env` |
| `starter/ollama_server.py` | Finds the running server and ignores a stale `OLLAMA_HOST` |
| `starter/main.py` | Loads `.env`, checks Ollama, runs the crew |
| `starter/llm.py` | Builds the local LLM from `.env` |
| `starter/crew.py` | Connects YAML names to Python methods and turns on the tool cache |
| `starter/settings.py` | Reads `starter/config/settings.yaml` |
| `starter/config/agents.yaml` | The card-guide role, model, and tools |
| `starter/config/tasks.yaml` | The question step and how many checker retries |
| `starter/config/settings.yaml` | How many search hits to return |
| `starter/tools/search_cards.py` | Keyword search over the cards |
| `starter/tools/read_card.py` | Read one card, confined to `cards/` |
| `starter/guardrail/answer_check.py` | Checks the finished answer against the named file |
| `starter/tools/example_tool.py` | Unused pattern for a new tool |
