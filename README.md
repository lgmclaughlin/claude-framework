# cframe

A CLI tool for scaffolding Claude-based projects with modular extensions.

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
