# Goblin Markdown Converter v1.0

A collection of tools for converting task lists exported from [Goblin Tools](https://goblin.tools/) into beautifully formatted Markdown files. This converter is specifically designed to work with the export format from Goblin Tools' Magic ToDo feature, preserving task hierarchies, time estimates, and category emojis.

## Quick Start

### Web Interface

The fastest way to convert your Goblin files is using our web interface:
[Goblin Markdown Web Converter](https://trentnford.com/goblin_markdown_web.html)

The web interface is built with vanilla JavaScript and HTML/CSS, providing a modern, responsive design with the following features:

- Drag and drop file upload
- Dark/light mode toggle
- Real-time conversion
- Multiple output formats (Markdown and Obsidian Canvas)
- Optional timestamp display
- Instant download of converted files
- No server-side processing - everything runs in your browser

Simply upload your `.goblin` or `.json` file and get your markdown instantly!

### Command Line Interface

For automated workflows or local usage:

```bash
python goblin_markdown_cli.py path/to/your/file.goblin
```

## Website

Visit the official website at [trentnford.com/goblin_markdown_web.html](https://trentnford.com/goblin_markdown_web.html) to use the web-based converter. The website provides a user-friendly interface for converting your Goblin Tools task lists to Markdown or Obsidian Canvas format without any installation required.

## Tools Included

1. `goblin_markdown_converter.py` - Core conversion library
2. `goblin_markdown_cli.py` - Command-line interface
3. `goblin_markdown_web.html` - Static web interface for browser-based conversion

## About Goblin Tools

[Goblin Tools](https://goblin.tools/) is a collection of AI-powered tools designed to help with various tasks. The Magic ToDo feature is particularly useful for breaking down complex tasks into manageable steps. This converter allows you to take those task lists and integrate them into your markdown-based workflow.

## Task Categories

Goblin Tools automatically assigns categories to top-level tasks, represented by emojis:

| Emoji | Category      | Description                              |
| ----- | ------------- | ---------------------------------------- |
| ☑️    | General       | Default category for uncategorized tasks |
| 🛠     | Technical     | Development and technical tasks          |
| 📋    | Organization  | Planning and organizational tasks        |
| 🎨    | Creative      | Design and artistic tasks                |
| 🏢    | Business      | Corporate and business-related tasks     |
| 📈    | Analytics     | Growth and data analysis tasks           |
| 🤝    | Social        | Collaboration and interpersonal tasks    |
| 📚    | Learning      | Research and educational tasks           |
| 🖊     | Writing       | Content creation tasks                   |
| 🎓    | Education     | Academic and teaching tasks              |
| 💬    | Communication | Discussion and messaging tasks           |
| 📝    | Documentation | Note-taking and documentation tasks      |
| 💵    | Financial     | Money and finance-related tasks          |

## Features

- Specifically designed for Goblin Tools export format
- Supports both `.json` and `.goblin` file formats from Goblin Tools
- Maintains task hierarchy with proper indentation
- Preserves time estimates in human-readable format
- Includes category emojis for root tasks
- Generates clean, well-formatted Markdown output
- Creates checkboxes for task tracking
- Preserves task completion status (checked/unchecked)
- Optional timestamp display for task creation dates
- Handles task ordering from the original file
- Converts between Markdown and Obsidian Canvas formats

## Requirements

- Python 3.x
- A task list exported from Goblin Tools

## Installation

1. Download the `goblin_markdown_cli.py` script to your computer
2. Make sure you have Python 3.x installed on your system

## Usage

### Command Line Usage

The command-line tool (`goblin_markdown_cli.py`) provides a simple way to convert your Goblin Tools task lists to Markdown or Obsidian Canvas format.

#### Basic Usage

```bash
python goblin_markdown_cli.py path/to/your/file.goblin
```

This will convert the specified file to Markdown format and save it with the same name but a `.md` extension.

#### Options

- `--timestamps` or `-t`: Include creation timestamps in the output
- `--canvas` or `-c`: Generate an Obsidian Canvas file instead of Markdown

#### Examples

1. Convert a Goblin file to Markdown:

   ```bash
   python goblin_markdown_cli.py magic_todo.goblin
   ```

2. Convert a JSON file to Markdown with timestamps:

   ```bash
   python goblin_markdown_cli.py tasks.json --timestamps
   ```

3. Convert a file to Obsidian Canvas format:

   ```bash
   python goblin_markdown_cli.py magic_todo.goblin --canvas
   ```

### Web Interface Usage

The web interface (`goblin_markdown_web.html`) provides a user-friendly way to convert your files without any installation:

1. Open the web interface in your browser
2. Drag and drop your `.goblin` or `.json` file
3. Select your desired output format (Markdown, Obsidian Canvas, or both)
4. Optionally enable timestamps
5. Click "Convert"
6. Download the converted file(s)

The web interface works entirely in your browser - no files are uploaded to any server.

## Input File Format

Your input file should be exported from Goblin Tools and contain tasks in the following format:

```json
[
  {
    "id": "unique_id",
    "text": "Task description",
    "estimate": 3600, // Time estimate in seconds (optional)
    "category": "🛠", // Emoji category (optional)
    "parentId": null, // null for root tasks, or ID of parent task
    "timestamp": 1234567890, // Creation timestamp (optional)
    "completed": false // Task completion status (optional)
  }
  // ... more tasks
]
```

## Output Format

The script generates a Markdown file with:

- A main "Tasks" heading
- Task hierarchies using proper indentation
- Checkboxes for task completion tracking (checked if completed in the original file)
- Time estimates in human-readable format (e.g., "2h 30m")
- Category emojis for root-level tasks
- Optional timestamps showing when tasks were created

Example output:

```markdown
# Tasks

## 🛠 Main Task (2h 30m)

- [ ] Subtask 1 (30m)
- [x] Subtask 2 (2h) (Created: 2023-07-15 14:30)
  - [ ] Sub-subtask A (1h)
  - [ ] Sub-subtask B (1h)
```

## Error Handling

The script includes error handling for:

- File not found
- Invalid JSON format
- Unsupported file extensions

## Examples

1. Convert a JSON file exported from Goblin Tools:

   ```bash
   python goblin_markdown_cli.py tasks.json
   ```

2. Convert a Goblin file exported from Goblin Tools:

   ```bash
   python goblin_markdown_cli.py magic_todo.goblin
   ```

3. Process a file in a different directory:

   ```bash
   python goblin_markdown_cli.py "path/to/my tasks.json"
   ```

4. Include timestamps in the output:
   ```bash
   python goblin_markdown_cli.py magic_todo.goblin --timestamps
   ```

## Notes

- The script automatically handles spaces in filenames
- Output files are created in the same directory as the input file
- Time estimates are optional and will be omitted if not provided
- Category emojis are optional and will be omitted if not provided
- Task completion status is preserved from the original file
- Timestamps are displayed in YYYY-MM-DD HH:MM format

## Credits

Created and maintained by Trent N. Ford ([@DrFretNot](https://github.com/DrFretNot)).

Visit my website at [trentnford.com](https://trentnford.com) for more information.

## License

MIT License

Copyright (c) 2025 Trent N. Ford

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
