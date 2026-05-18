#!/usr/bin/env python3
"""
Knowledge Extraction and Wiki Update Script

This script:
1. Reads input text from workflow dispatch or inbox files
2. Calls OpenRouter API to extract structured entities (definitions, facts, research)
3. Updates the repository wiki with the extracted entities
"""

import os
import sys
import json
import time
import subprocess
import re
from datetime import datetime
from pathlib import Path

import requests


# Configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openrouter/free"  # Free model router
DEFAULT_PROMPT_TEMPLATE = """You are a precise data extraction tool. Your entire response must be a single valid JSON object and nothing else. Do not include any markdown formatting, explanations, or code fences.

Your task is to analyze text and extract three types of entities:

1. DEFINITIONS: Explanations of terms, concepts, or specialized vocabulary
2. FACTS: Verifiable statements, data points, or established information  
3. RESEARCH: Insights, hypotheses, study results, or emerging findings

Return your analysis as a JSON object with exactly three arrays: "definitions", "facts", and "research".
Each item should have a "text" field (the extracted content) and optionally a "context" field (additional relevant information).

Example format:
{
  "definitions": [
    {"text": "Term explanation", "context": "Related concept"}
  ],
  "facts": [
    {"text": "Verifiable statement"}
  ],
  "research": [
    {"text": "Research insight", "context": "Study reference"}
  ]
}

CRITICAL: Output ONLY the raw JSON object. No markdown, no code blocks, no explanations."""
MAX_RETRIES = 3
RETRY_DELAY_BASE = 2  # seconds


def log(message: str):
    """Print a log message."""
    print(f"[INFO] {message}")


def log_error(message: str):
    """Print an error message."""
    print(f"[ERROR] {message}", file=sys.stderr)


def get_input_text() -> tuple[str, str]:
    """
    Get input text and source label from environment variables.
    
    Returns:
        Tuple of (text, source_label)
    """
    # Check for manual dispatch input
    manual_text = os.environ.get("INPUT_TEXT", "").strip()
    manual_source = os.environ.get("INPUT_SOURCE", "").strip()
    
    if manual_text:
        source = manual_source if manual_source else "manual"
        return manual_text, source
    
    # Check for file-based input
    inbox_path = os.environ.get("INBOX_PATH", "inbox").strip()
    file_pattern = os.environ.get("FILE_PATTERN", "").strip()
    
    if not inbox_path:
        inbox_path = "inbox"
    
    if file_pattern:
        # Specific file triggered the workflow
        matching_files = list(Path(inbox_path).glob(file_pattern))
        if matching_files:
            txt_file = matching_files[0]
            content = txt_file.read_text(encoding="utf-8").strip()
            source = txt_file.stem  # filename without extension
            if content:
                return content, source
    
    # Look for any .txt files in inbox
    inbox_dir = Path(inbox_path)
    if inbox_dir.exists():
        txt_files = sorted(inbox_dir.glob("*.txt"))
        if txt_files:
            # Process the most recently modified file
            txt_file = max(txt_files, key=lambda f: f.stat().st_mtime)
            content = txt_file.read_text(encoding="utf-8").strip()
            source = txt_file.stem
            if content:
                return content, source
    
    return "", ""


def call_openrouter(text: str, strict_json: bool = False) -> dict | None:
    """
    Call OpenRouter API to extract entities from text.
    
    Args:
        text: The input text to process
        strict_json: If True, use stricter prompt for retry
        
    Returns:
        Parsed JSON response or None on failure
    """
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        log_error("OPENROUTER_API_KEY environment variable not set")
        return None
    
    model = os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL)
    prompt_template = os.environ.get("OPENROUTER_PROMPT_TEMPLATE", DEFAULT_PROMPT_TEMPLATE)
    
    # Get repo URL for HTTP-Referer header
    github_server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    github_repo = os.environ.get("GITHUB_REPOSITORY", "unknown/repo")
    repo_url = f"{github_server}/{github_repo}"
    
    # Build merged user message with clear instruction
    if strict_json:
        user_prompt = f"""You are a knowledge extraction assistant. Extract entities from the provided text.
Return ONLY a valid JSON object with exactly this structure - no other text:
{{
  "definitions": [{{"text": "...", "context": "..."}}],
  "facts": [{{"text": "...", "context": "..."}}],
  "research": [{{"text": "...", "context": "..."}}]
}}
Each array may be empty. Each item must have 'text' field and optionally 'context'.
Do not include any markdown formatting, code blocks, or explanations.

Text to analyze:
{text}"""
    else:
        user_prompt = f"""{prompt_template}

Text to analyze:
{text}"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": repo_url,
        "X-Title": "Knowledge Extractor"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 24000,
        "response_format": {"type": "json_object"},
        "provider": {"require_parameters": True},
        "plugins": [{"id": "response-healing"}]
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            log(f"Calling OpenRouter API (attempt {attempt + 1}/{MAX_RETRIES})...")
            response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=60)
            
            # Check HTTP status code first - handle different error codes appropriately
            if response.status_code == 403:
                log_error("HTTP 403 Forbidden received from OpenRouter API")
                log_error("Please check the following:")
                log_error("  1. OPENROUTER_API_KEY secret is valid and has credits")
                log_error("  2. OPENROUTER_MODEL variable specifies an accessible free model")
                log_error(f"     Current model: {model}")
                log_error("     Note: 'openrouter/free' is a special router that auto-selects a free model")
                log_error("  3. Required headers (Authorization, Content-Type, HTTP-Referer, X-Title) are set correctly")
                log_error(f"     HTTP-Referer: {repo_url}")
                log_error("  4. Model is available at https://openrouter.ai/models?q=free")
                return None
            
            # Handle rate limiting (429) and service unavailable (503) with retry
            if response.status_code in [429, 503]:
                log_error(f"HTTP {response.status_code} received - rate limit or service issue")
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAY_BASE * (2 ** attempt) * 2  # Longer delay for rate limits
                    log(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                    continue
                else:
                    log_error(f"Max retries reached after HTTP {response.status_code}")
                    return None
            
            # For other non-200 status codes, try to get more info but don't treat as success
            if response.status_code != 200:
                log_error(f"Unexpected HTTP status code: {response.status_code}")
                log_error(f"Response body: {response.text[:500]}")
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAY_BASE * (2 ** attempt)
                    log(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                    continue
                else:
                    return None
            
            # Validate response body is not empty before parsing
            if not response.text or len(response.text.strip()) == 0:
                log_error("Empty response body from API (HTTP 200 but no content)")
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAY_BASE * (2 ** attempt)
                    log(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                continue
            
            result = response.json()
            choices = result.get("choices", [])
            if not choices:
                log_error("No choices in API response")
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAY_BASE * (2 ** attempt)
                    log(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                continue
            
            choice = choices[0]
            finish_reason = choice.get("finish_reason", "")
            content = choice.get("message", {}).get("content", "")
            
            # Validate finish_reason is "stop" (not "length")
            if finish_reason == "length":
                log_error("Response truncated due to max_tokens limit (finish_reason: length)")
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAY_BASE * (2 ** attempt)
                    log(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                continue
            
            if not content:
                log_error("Empty response from API (no content in choices)")
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAY_BASE * (2 ** attempt)
                    log(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                continue
            
            # Try to parse JSON
            parsed = parse_json_response(content)
            if parsed:
                return parsed
            
            log_error(f"Failed to parse JSON from response: {content[:200]}...")
            
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAY_BASE * (2 ** attempt)
                log(f"Retrying in {delay} seconds...")
                time.sleep(delay)
        except requests.exceptions.Timeout as e:
            log_error(f"API request timed out: {e}")
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAY_BASE * (2 ** attempt)
                log(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return None
        except requests.exceptions.RequestException as e:
            log_error(f"API request failed: {e}")
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAY_BASE * (2 ** attempt)
                log(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return None
    
    return None


def parse_json_response(content: str) -> dict | None:
    """
    Parse JSON from API response, handling potential markdown formatting.
    
    Args:
        content: Raw response content
        
    Returns:
        Parsed JSON dict or None
    """
    # Remove markdown code blocks if present - handle both ```json and ``` variants
    content = content.strip()
    
    # Try to extract JSON from markdown code blocks (more robust pattern)
    json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', content, re.DOTALL)
    if json_match:
        content = json_match.group(1)
    
    # If still wrapped in backticks or has prefix text, find the first JSON object
    if not content.startswith('{'):
        # Find the first { and last } to extract the complete JSON object
        brace_match = re.search(r'\{.*\}', content, re.DOTALL)
        if brace_match:
            content = brace_match.group(0)
    
    try:
        data = json.loads(content)
        # Validate structure
        if not isinstance(data, dict):
            return None
        for key in ["definitions", "facts", "research"]:
            if key not in data or not isinstance(data[key], list):
                return None
        return data
    except json.JSONDecodeError:
        # Log the problematic content for debugging (first 200 chars)
        log_error(f"JSON decode error. Content starts with: {content[:200]}")
        return None


def clone_wiki(repo_url: str, wiki_dir: Path) -> bool:
    """
    Clone the repository wiki.
    
    Args:
        repo_url: Base repository URL
        wiki_dir: Directory to clone into
        
    Returns:
        True on success, False on failure
    """
    token = os.environ.get("WIKI_PUSH_TOKEN", "")
    if not token:
        log_error("WIKI_PUSH_TOKEN environment variable not set")
        return False
    
    wiki_url = f"{repo_url}.wiki.git"
    
    # Insert token for authentication
    auth_url = wiki_url.replace("https://", f"https://{token}@")
    
    try:
        log(f"Cloning wiki from {wiki_url}...")
        subprocess.run(
            ["git", "clone", "--depth", "1", auth_url, str(wiki_dir)],
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"Failed to clone wiki: {e.stderr}")
        return False


def read_wiki_page(wiki_dir: Path, page_name: str) -> str:
    """
    Read content of a wiki page.
    
    Args:
        wiki_dir: Wiki directory
        page_name: Page name (without .md extension)
        
    Returns:
        Page content or empty string if doesn't exist
    """
    page_path = wiki_dir / f"{page_name}.md"
    if page_path.exists():
        return page_path.read_text(encoding="utf-8")
    return ""


def write_wiki_page(wiki_dir: Path, page_name: str, content: str):
    """
    Write content to a wiki page.
    
    Args:
        wiki_dir: Wiki directory
        page_name: Page name (without .md extension)
        content: Page content
    """
    page_path = wiki_dir / f"{page_name}.md"
    page_path.write_text(content, encoding="utf-8")


def append_entities_to_page(existing_content: str, entities: list[dict], date_str: str, source: str) -> str:
    """
    Append entities to wiki page content, avoiding duplicates.
    
    Args:
        existing_content: Current page content
        entities: List of entity dicts with 'text' and optional 'context'
        date_str: Date string for heading
        source: Source label
        
    Returns:
        Updated page content
    """
    if not entities:
        return existing_content
    
    heading = f"## {date_str} – {source}"
    
    # Build new entries
    new_entries = []
    for entity in entities:
        text = entity.get("text", "").strip()
        context = entity.get("context", "").strip()
        
        if not text:
            continue
        
        # Format entry
        if context:
            entry = f"- **{text}** *(context: {context})*"
        else:
            entry = f"- **{text}**"
        
        # Check for duplicate in existing content under same date/source
        if heading in existing_content and entry in existing_content:
            log(f"Skipping duplicate entry: {text[:50]}...")
            continue
        
        new_entries.append(entry)
    
    if not new_entries:
        return existing_content
    
    # Build updated content
    if not existing_content.strip():
        # New page - add title
        category = "Knowledge Base"
        if "Definitions" in str(entities):
            category = "Definitions"
        content = f"# {category}\n\n"
    else:
        content = existing_content.rstrip() + "\n\n"
    
    content += f"{heading}\n"
    for entry in new_entries:
        content += f"{entry}\n"
    
    return content


def update_wiki(wiki_dir: Path, extracted_data: dict, date_str: str, source: str) -> bool:
    """
    Update wiki pages with extracted entities.
    
    Args:
        wiki_dir: Wiki directory
        extracted_data: Dict with definitions, facts, research arrays
        date_str: Date string for headings
        source: Source label
        
    Returns:
        True on success, False on failure
    """
    pages = {
        "Definitions": extracted_data.get("definitions", []),
        "Facts": extracted_data.get("facts", []),
        "Research": extracted_data.get("research", [])
    }
    
    updates_needed = False
    for page_name, entities in pages.items():
        if not entities:
            continue
        
        existing = read_wiki_page(wiki_dir, page_name)
        updated = append_entities_to_page(existing, entities, date_str, source)
        
        if updated != existing:
            write_wiki_page(wiki_dir, page_name, updated)
            updates_needed = True
            log(f"Updated {page_name}.md")
    
    return updates_needed


def push_wiki_changes(wiki_dir: Path, source: str) -> bool:
    """
    Commit and push wiki changes.
    
    Args:
        wiki_dir: Wiki directory
        source: Source label for commit message
        
    Returns:
        True on success, False on failure
    """
    token = os.environ.get("WIKI_PUSH_TOKEN", "")
    if not token:
        log_error("WIKI_PUSH_TOKEN not set")
        log_error("Please ensure the WIKI_PUSH_TOKEN secret is configured with a GitHub classic token.")
        log_error("The token must have 'repo' and 'wiki' scopes.")
        log_error("Create token at: https://github.com/settings/tokens/new (select 'Classic' token)")
        return False
    
    try:
        # Configure git user
        subprocess.run(
            ["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"],
            cwd=wiki_dir,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.name", "github-actions[bot]"],
            cwd=wiki_dir,
            check=True,
            capture_output=True
        )
        
        # Stage all changes
        subprocess.run(
            ["git", "add", "-A"],
            cwd=wiki_dir,
            check=True,
            capture_output=True
        )
        
        # Check if there are changes to commit
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=wiki_dir,
            check=True,
            capture_output=True,
            text=True
        )
        
        if not status_result.stdout.strip():
            log("No wiki changes to commit")
            return True
        
        # Commit
        commit_msg = f"Update wiki from: {source}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=wiki_dir,
            check=True,
            capture_output=True
        )
        
        # Prepare remote URL with token - always set it to ensure authentication
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=wiki_dir,
            check=True,
            capture_output=True,
            text=True
        )
        remote_url = result.stdout.strip()
        
        # Always insert token for authentication (in case it was cloned without token)
        if "@" not in remote_url:
            auth_url = remote_url.replace("https://", f"https://{token}@")
            subprocess.run(
                ["git", "remote", "set-url", "origin", auth_url],
                cwd=wiki_dir,
                check=True,
                capture_output=True
            )
            log("Set authenticated remote URL")
        
        # Push with conflict handling
        for attempt in range(2):
            try:
                subprocess.run(
                    ["git", "push", "origin", "master"],
                    cwd=wiki_dir,
                    check=True,
                    capture_output=True,
                    text=True
                )
                log("Wiki changes pushed successfully")
                return True
            except subprocess.CalledProcessError as e:
                error_output = e.stderr or ""
                # Check for 403 permission denied specifically
                if "403" in error_output or "permission denied" in error_output.lower():
                    log_error("HTTP 403 Permission Denied when pushing to wiki")
                    log_error("The WIKI_PUSH_TOKEN does not have proper permissions.")
                    log_error("Required fixes:")
                    log_error("  1. Create a NEW classic token at: https://github.com/settings/tokens/new")
                    log_error("  2. Select scopes: 'repo' (or 'public_repo') AND 'wiki'")
                    log_error("  3. Ensure the token owner has write access to the repository")
                    log_error("  4. Update the WIKI_PUSH_TOKEN secret in repository Settings > Secrets > Actions")
                    return False
                
                if "rejected" in error_output.lower() and attempt == 0:
                    log("Push rejected, attempting rebase...")
                    subprocess.run(
                        ["git", "pull", "--rebase", "origin", "master"],
                        cwd=wiki_dir,
                        check=True,
                        capture_output=True
                    )
                    subprocess.run(
                        ["git", "push", "origin", "master"],
                        cwd=wiki_dir,
                        check=True,
                        capture_output=True
                    )
                    log("Wiki changes pushed after rebase")
                    return True
                else:
                    log_error(f"Failed to push wiki changes: {error_output}")
                    return False
                    
    except subprocess.CalledProcessError as e:
        log_error(f"Git operation failed: {e.stderr if hasattr(e, 'stderr') else e}")
        return False
    except Exception as e:
        log_error(f"Unexpected error pushing wiki: {e}")
        return False


def main():
    """Main entry point."""
    log("Starting knowledge extraction workflow...")
    
    # Get input
    text, source = get_input_text()
    
    if not text:
        log("No input text provided. Exiting gracefully.")
        sys.exit(0)
    
    log(f"Processing input from source: {source}")
    log(f"Text length: {len(text)} characters")
    
    # Call OpenRouter
    extracted = call_openrouter(text, strict_json=False)
    
    if not extracted:
        log("First attempt failed, retrying with strict JSON mode...")
        extracted = call_openrouter(text, strict_json=True)
    
    if not extracted:
        log_error("Failed to extract entities from text after retries")
        sys.exit(1)
    
    # Validate extracted data
    total_entities = (
        len(extracted.get("definitions", [])) +
        len(extracted.get("facts", [])) +
        len(extracted.get("research", []))
    )
    log(f"Extracted {total_entities} entities:")
    log(f"  - Definitions: {len(extracted.get('definitions', []))}")
    log(f"  - Facts: {len(extracted.get('facts', []))}")
    log(f"  - Research: {len(extracted.get('research', []))}")
    
    if total_entities == 0:
        log("No entities extracted. Nothing to add to wiki.")
        sys.exit(0)
    
    # Get repository URL from environment
    repo_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo_name = os.environ.get("GITHUB_REPOSITORY", "")
    if repo_name:
        wiki_url = f"{repo_url}/{repo_name}"
    else:
        log_error("GITHUB_REPOSITORY not set")
        sys.exit(1)
    
    # Clone wiki
    wiki_dir = Path("/tmp/wiki_checkout")
    if wiki_dir.exists():
        subprocess.run(["rm", "-rf", str(wiki_dir)], check=True)
    
    if not clone_wiki(wiki_url, wiki_dir):
        sys.exit(1)
    
    # Update wiki pages
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    
    if not update_wiki(wiki_dir, extracted, date_str, source):
        log("No wiki updates needed (all entries may be duplicates)")
        sys.exit(0)
    
    # Push changes
    if not push_wiki_changes(wiki_dir, source):
        sys.exit(1)
    
    log("Knowledge extraction complete!")


if __name__ == "__main__":
    main()
