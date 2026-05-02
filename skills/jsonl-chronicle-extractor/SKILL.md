---
name: jsonl-chronicle-extractor
description: Extracts multi-line Session Chronicle entries from JSONL files by parsing JSON objects and matching a regex pattern within nested 'text' fields. Use when you need to specifically extract narrative blocks from structured JSONL logs or progressive response files.
---

# JSONL Chronicle Extractor

## Overview

This skill provides a script to extract specific multi-line text content, such as "Session Chronicles", embedded within JSON objects stored in `.jsonl` files. It's designed to navigate nested JSON structures and extract narrative blocks based on a provided regular expression.

## Usage

The primary functionality is exposed via the `extract_chronicle.js` script located in the `scripts/` directory.

### `scripts/extract_chronicle.js`

This script reads a `.jsonl` file, parses each line as a JSON object, and then searches within the `message.content[].text` fields for a specified regular expression pattern. If a match is found, the entire content of that `text` field (which typically contains the full chronicle) is extracted.

**Arguments:**
1.  `<file_path>`: The absolute or relative path to the `.jsonl` file to process.
2.  `<regex_pattern>`: A regular expression (JavaScript-compatible) to match against the `text` content of the chronicle.

**Example Command:**

```bash
node scripts/extract_chronicle.js /path/to/your/file.jsonl "^## 🌊 Session Chronicle — Fe[br]* 28, 2026"
```

**Output:**

The script prints the extracted chronicle(s) to standard output. If multiple chronicles are found, they will be separated by `\n---\n`. If no chronicles match the pattern, a message indicating this will be printed.

## Example Pattern for Session Chronicles

For extracting "Session Chronicle" entries like "🌊 Session Chronicle — February 28, 2026" or "🌊 Session Chronicle — Feb 28, 2026", a robust pattern is:

`^## 🌊 Session Chronicle — Fe[br]* 28, 2026`

This pattern accounts for variations in the month name (February/Feb) and ensures it matches the start of the chronicle header.

## Resources

This skill includes the following script:

### `scripts/`
- `extract_chronicle.js`: The core script for parsing JSONL files and extracting chronicle content.
