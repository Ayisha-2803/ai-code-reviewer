import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def parse_github_pr_url(pr_url):
    parts = pr_url.strip("/").split("/")
    owner = parts[-4]
    repo = parts[-3]
    pr_number = parts[-1]
    return owner, repo, pr_number

def get_pr_diff(owner, repo, pr_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")
    files = response.json()
    diff_text = ""
    for f in files:
        filename = f.get("filename", "")
        patch = f.get("patch", "")
        if patch:
            diff_text += f"\n\n### File: {filename}\n```\n{patch}\n```"
    return diff_text, files

def get_pr_info(owner, repo, pr_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code}")
    data = response.json()
    return {
        "title": data.get("title", ""),
        "description": data.get("body", "") or "No description provided.",
        "author": data.get("user", {}).get("login", ""),
        "base_branch": data.get("base", {}).get("ref", ""),
        "head_branch": data.get("head", {}).get("ref", "")
    }

def review_code_with_openrouter(diff_text, pr_info):
    prompt = f"""You are an expert senior software engineer performing a thorough code review.

PR Title: {pr_info['title']}
Author: {pr_info['author']}
Branch: {pr_info['head_branch']} → {pr_info['base_branch']}
Description: {pr_info['description']}

Here are the code changes:
{diff_text}

Please provide a comprehensive code review with the following sections:

## 🔍 Summary
Brief overview of what this PR does.

## 🐛 Bugs & Issues
List any bugs, logic errors, or incorrect behavior you find. If none, say "No bugs found."

## 🔒 Security Vulnerabilities
Identify any security issues like SQL injection, XSS, hardcoded secrets, insecure dependencies, etc. If none, say "No security issues found."

## ⚡ Performance Issues
Identify inefficient code, unnecessary loops, missing indexes, memory leaks, etc. If none, say "No performance issues found."

## 🧹 Code Quality & Smells
Comment on naming conventions, code duplication, overly complex logic, missing error handling, etc.

## ✅ Good Practices
Highlight what was done well in this PR.

## 📋 Actionable Recommendations
List specific, numbered action items the developer should address before merging.

## 🏆 Overall Score
Rate this PR: Excellent / Good / Needs Work / Major Issues
And give a one-line verdict.

## 🚨 ISSUES SUMMARY TABLE
At the very end, provide a compact summary table in this EXACT format (one issue per line):
ISSUE_START
TYPE: Security | SEVERITY: Critical | ISSUE: Hardcoded secret key | FIX: Use environment variables
TYPE: Security | SEVERITY: Critical | ISSUE: SQL Injection in login() | FIX: Use parameterized queries
TYPE: Performance | SEVERITY: Medium | ISSUE: Large loop in get_all_data() | FIX: Use generators or pagination
ISSUE_END

Only include real issues found. Use severity: Critical, High, Medium, or Low.
"""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/auto",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    if response.status_code != 200:
        raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"]

def parse_issues_table(review_text):
    """Extract structured issues from the ISSUE_START...ISSUE_END block."""
    issues = []
    try:
        start = review_text.index("ISSUE_START") + len("ISSUE_START")
        end = review_text.index("ISSUE_END")
        block = review_text[start:end].strip()
        for line in block.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = {}
            for segment in line.split("|"):
                segment = segment.strip()
                if ":" in segment:
                    key, val = segment.split(":", 1)
                    parts[key.strip()] = val.strip()
            if parts:
                issues.append(parts)
    except (ValueError, Exception):
        pass
    return issues

def post_review_comment(owner, repo, pr_number, review_text):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    # Clean the raw table from the GitHub comment
    clean_review = review_text
    try:
        end = review_text.index("ISSUE_START")
        clean_review = review_text[:end].strip()
    except ValueError:
        pass
    body = f"## 🤖 AI Code Review by ReviewBot\n\n{clean_review}\n\n---\n*Powered by AI via OpenRouter*"
    response = requests.post(url, headers=HEADERS, json={"body": body})
    if response.status_code == 201:
        return True, response.json().get("html_url", "")
    else:
        return False, response.text

def run_review(pr_url, post_to_github=False):
    owner, repo, pr_number = parse_github_pr_url(pr_url)
    pr_info = get_pr_info(owner, repo, pr_number)
    diff_text, files = get_pr_diff(owner, repo, pr_number)

    if not diff_text.strip():
        return {"error": "No code changes found in this PR."}

    review = review_code_with_openrouter(diff_text, pr_info)
    issues = parse_issues_table(review)

    # Remove raw table block from display text
    display_review = review
    try:
        end = review.index("ISSUE_START")
        display_review = review[:end].strip()
    except ValueError:
        pass

    result = {
        "pr_title": pr_info["title"],
        "author": pr_info["author"],
        "files_changed": len(files),
        "review": display_review,
        "issues": issues,
        "posted_to_github": False,
        "comment_url": ""
    }

    if post_to_github:
        success, url = post_review_comment(owner, repo, pr_number, review)
        result["posted_to_github"] = success
        result["comment_url"] = url

    return result
