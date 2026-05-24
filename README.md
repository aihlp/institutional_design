# institutional_design

Automated Knowledge Extraction to GitHub Wiki via GitHub Actions.

## Overview

This repository implements a GitHub Actions workflow that:
1. Accepts user-submitted text (manually or via `.txt` files in the `inbox/` folder)
2. Sends it to an LLM via OpenRouter to extract structured entities
3. Automatically appends them to the repository's wiki in a well-organized manner

## Setup

### Prerequisites

1. Enable GitHub Wiki for your repository
2. Configure the following secrets in **Settings → Secrets and variables → Actions**:
   - `OPENROUTER_API_KEY` – API key for OpenRouter
   - `WIKI_PUSH_TOKEN` – GitHub personal access token (classic) with `repo` and `wiki` scopes

### Creating WIKI_PUSH_TOKEN

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with scopes:
   - `repo` (Full control of private repositories)
   - `write:org` (if using organization repos)
3. Copy the token and add it as `WIKI_PUSH_TOKEN` secret

## Usage

### Method 1: Manual Dispatch

1. Go to **Actions** tab
2. Select **"Knowledge Extraction to Wiki"** workflow
3. Click **"Run workflow"**
4. Fill in:
   - **Text**: Paste the text you want to process
   - **Source** (optional): A label for the source (e.g., "Meeting Notes", "Research Paper")
5. Click **"Run workflow"**

### Method 2: File-based Input

1. Create a `.txt` file in the `inbox/` folder at the repository root
2. The filename (without extension) will be used as the source label
3. Push the file to the repository
4. The workflow triggers automatically

Example:
```bash
echo "Your knowledge content here..." > inbox/research_notes.txt
git add inbox/research_notes.txt
git commit -m "Add research notes for processing"
git push
```

## Output

The workflow extracts knowledge organized into **two fundamental dimensions**: Basic (static) parts and Dynamic (relational) parts.

### Basic (Static) Parts - Constituent Elements:
- **Definitions**: Explanations of terms, concepts, or specialized vocabulary; foundational conceptual primitives
- **Facts**: Verifiable statements, data points, empirical observations, or established information
- **Concepts**: Abstract ideas, theoretical constructs, or mental models that organize thinking
- **Entities**: Concrete objects, actors, organizations, or identifiable things in the domain
- **Contexts**: Situational conditions, environmental factors, or boundary conditions that shape meaning

### Dynamic (Relational) Parts - Connections and Flows:
- **Relationships**: Connections, associations, or links between entities/concepts (e.g., "causes", "influences", "part-of")
- **Processes**: Sequences of actions, transformations, or temporal flows that describe how things change
- **Mechanisms**: Causal pathways, explanatory logics, or functional operations that produce outcomes

These are appended to corresponding wiki pages:
- `Definitions.md`, `Facts.md`, `Concepts.md`, `Entities.md`, `Contexts.md` (basic parts)
- `Relationships.md`, `Processes.md`, `Mechanisms.md` (dynamic parts with relinking)
- `Home.md` (automatically generated index with cross-references)

Dynamic entries include **relinking** via wiki-style `[[source]] → [[target]]` notation to enable navigation between connected knowledge elements.

## Files

- `.github/workflows/knowledge.yml` – GitHub Actions workflow definition
- `process_and_update.py` – Main processing script
- `requirements.txt` – Python dependencies
- `inbox/` – Folder for file-based input

## Error Handling

- Network/API failures: Retries up to 3 times with exponential backoff
- Invalid JSON from LLM: Retries once with stricter prompt
- Wiki push conflicts: Performs git pull --rebase and retries
- Empty input: Exits gracefully without error

## Security

- Secrets are never exposed in logs
- API calls use secure environment variables
- Wiki authentication uses token-based auth