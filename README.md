# cframe

A CLI tool for managing Claude-based projects.

Structure your Claude Code projects with phase-based planning, progress tracking, and archival so long-running projects stay organized across sessions.

## Installation

### Linux / macOS

```bash
./install.sh
```

Add to PATH if needed:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Windows

Double-click `install.bat` or run from command line:

```cmd
install.bat
```

Or directly in PowerShell:

```powershell
.\install.ps1
```

Requires Python 3 installed and in PATH.

> **Note:** macOS and Windows support is untested. Please open an issue if you encounter problems.

## Usage

### Create a new project directory

```bash
cframe init my-project
cframe init my-project --design --systems
```

### Add to existing project directory

```bash
# From inside
cframe init

# From outside
cframe init path/to/existing-project
```

### Add extensions

```bash
cframe add --deploy
```

### List available extensions

```bash
cframe list
```

### Show project status

```bash
cframe status
```

## Suggested Workflow

1. Run `cframe init` and update `.claude/OVERVIEW.md` with a project summary and deliverables
2. Run Claude in plan mode and collaborate to define phases and high-level tasks in OVERVIEW
3. Plan the first `CURRENT_PHASE` using OVERVIEW as reference; include details, edge cases, and granular tasks
4. Optionally add extensions (`cframe add --deploy`) and populate their md files with specs
5. Iterate until CURRENT_PHASE is complete
6. Repeat for each phase until the project is finalized

> **Tip:** Some extensions are self-updating. For example, `--deploy` updates automatically when Claude recognizes deployment-relevant steps.

## Extensions

| Extension | Description |
|-----------|-------------|
| `--design` | UI/UX design planning and documentation |
| `--deploy` | Deployment steps and documentation |
| `--systems` | System architecture and infrastructure |

## Project Structure

After `cframe init`, your project contains:

```
.claude/
  extensions.json    # Installed extensions
  OVERVIEW.md        # Project roadmap
  CURRENT_PHASE.md   # Active work
  PROGRESS.md        # Progress log
  PROMPT.md          # Large prompt input
  archive/           # Historical records
CLAUDE.md            # Claude instructions
```

## License

MIT
