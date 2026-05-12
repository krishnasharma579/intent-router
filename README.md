# intent-router

A lightweight intent-classification router that maps user input into one of three routes:

- `hardware_query`
- `code_generation`
- `general_chat`

## Project Structure

- `/core`: configuration loading and LLM client setup
- `/prompts`: router system prompt
- `/router`: schema and intent classification logic
- `test_router.py`: manual smoke-test runner
- `/tests`: pytest unit tests

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy the environment template and set your key:

   ```bash
   cp .env.example .env
   ```

4. Update `.env` with a valid `GROQ_API_KEY`.

## Configuration

Supported environment variables:

- `GROQ_API_KEY` (required)
- `MODEL_NAME` (optional, default: `llama-3.1-8b-instant`)
- `ROUTER_TEMPERATURE` (optional, default: `0.0`, valid range `0.0-2.0`)

## Usage

### Classify a query

```python
from router import classify_intent

intent = classify_intent("Write Arduino code to blink an LED")
print(intent)
```

### Run manual smoke tests

```bash
python test_router.py
```

### Run unit tests

```bash
python -m pytest -q
```
