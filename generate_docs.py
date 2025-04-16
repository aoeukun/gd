import os
import json
import requests
from pathlib import Path
import yaml
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

SYSTEM_PROMPT = """You are an expert technical writer and software engineer.

Given the following Python code, generate clear, concise, and professional documentation in Markdown format.

- For each function or class:
  - Explain what it does, its purpose, and use cases
  - Include input parameters with types and descriptions
  - Describe the return value with type and meaning
  - Mention any side effects, exceptions, or special behaviors
  - Write in a friendly, human-readable tone for developers
  - Format the output using Markdown with proper headers, bullet points, and code blocks
  - If there is no function or class, don't generate anything.
"""

def call_groq(code: str) -> str:
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"```python\n{code}\n```"}
        ]
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def generate_docs(code_path: Path, output_path: Path):
    code = code_path.read_text(encoding="utf-8")
    documentation = call_groq(code)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(f"# Documentation for `{code_path.name}`\n\n{documentation}", encoding="utf-8")

def update_mkdocs_yml():
    GENERATED_DIR = Path("docs/generated")
    MKDOCS_YML_PATH = Path("mkdocs.yml")

    with open(MKDOCS_YML_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    files = [f for f in GENERATED_DIR.iterdir() if f.suffix == ".md"]
    files.sort()

    # Clean old "Generated Docs" section if it exists
    new_nav = []
    for item in config.get("nav", []):
        if isinstance(item, dict) and "Generated Docs" in item:
            continue
        new_nav.append(item)

    # Build new section
    generated_section = {"Generated Docs": []}
    for file in files:
        title = file.stem.replace("_", " ").title()
        generated_section["Generated Docs"].append({title: f"generated/{file.name}"})

    new_nav.append(generated_section)
    config["nav"] = new_nav

    with open(MKDOCS_YML_PATH, "w", encoding="utf-8") as f:
        yaml.dump(config, f, sort_keys=False)

    print("✅ mkdocs.yml updated successfully.")

def main():
    src_dir = Path("src")
    out_dir = Path("docs/generated")

    for file in src_dir.rglob("*.py"):
        generate_docs(file, out_dir / f"{file.stem}.md")

    update_mkdocs_yml()
    print("🎉 Documentation generated and mkdocs navigation updated.")

if __name__ == "__main__":
    main()
