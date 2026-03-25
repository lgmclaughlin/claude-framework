#!/usr/bin/env python3
"""cframe - CLI tool for initializing and managing Claude-based project structures."""

import argparse
import json
import shutil
import sys
from pathlib import Path


def die(message: str) -> None:
    """Print error message and exit."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def get_template_dir() -> Path:
    """Resolve path to templates/ directory."""
    # Check installed location first
    installed_dir = Path.home() / ".local" / "share" / "cframe" / "templates"
    if installed_dir.exists():
        return installed_dir

    # Fall back to relative path (development mode)
    script_dir = Path(__file__).resolve().parent
    dev_dir = script_dir.parent / "templates"
    if dev_dir.exists():
        return dev_dir

    die("Templates directory not found. Run install.sh or check your installation.")


def get_registry() -> dict:
    """Load and parse the extension registry."""
    registry_path = get_template_dir() / "extensions" / "registry.json"
    try:
        with open(registry_path) as f:
            return json.load(f)
    except FileNotFoundError:
        die(f"Registry not found: {registry_path}")
    except json.JSONDecodeError as e:
        die(f"Invalid registry.json: {e}")


def get_extensions_file(project_dir: Path = None) -> dict:
    """Read .claude/extensions.json from project directory."""
    if project_dir is None:
        project_dir = Path.cwd()
    extensions_path = project_dir / ".claude" / "extensions.json"
    try:
        with open(extensions_path) as f:
            return json.load(f)
    except FileNotFoundError:
        die(f"Extensions file not found: {extensions_path}")
    except json.JSONDecodeError as e:
        die(f"Invalid extensions.json: {e}")


def save_extensions_file(data: dict, project_dir: Path = None) -> None:
    """Write updated extensions.json to project directory."""
    if project_dir is None:
        project_dir = Path.cwd()
    extensions_path = project_dir / ".claude" / "extensions.json"
    try:
        with open(extensions_path, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
    except PermissionError:
        die(f"Permission denied: {extensions_path}")


def is_valid_project(project_dir: Path = None) -> bool:
    """Check if directory is a valid cframe project."""
    if project_dir is None:
        project_dir = Path.cwd()
    return (project_dir / ".claude" / "extensions.json").exists()


def copy_directory(src: Path, dst: Path) -> None:
    """Recursively copy directory contents, preserving structure."""
    try:
        for item in src.iterdir():
            target = dst / item.name
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                copy_directory(item, target)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
    except PermissionError as e:
        die(f"Permission denied: {e.filename}")


def apply_extensions(extensions: list[str], project_dir: Path) -> None:
    """Apply extensions to a project. Used by both init and add."""
    registry = get_registry()
    available = registry.get("extensions", {})
    installed = get_extensions_file(project_dir).get("extensions", [])
    extensions_dir = get_template_dir() / "extensions"
    claude_md_path = project_dir / "CLAUDE.md"

    # Add header only if this is the first extension
    needs_header = len(installed) == 0

    for ext_name in extensions:
        # Validate extension exists
        if ext_name not in available:
            die(f"Unknown extension '{ext_name}'")

        # Skip if already installed
        if ext_name in installed:
            print(f"Skipping '{ext_name}' (already installed)")
            continue

        ext_path = extensions_dir / ext_name

        # Copy extension files/ into project root
        files_dir = ext_path / "files"
        if files_dir.exists():
            copy_directory(files_dir, project_dir)

        # Append to CLAUDE.md
        append_file = ext_path / "CLAUDE.md.append"
        if append_file.exists():
            claude_md_content = claude_md_path.read_text()

            # Add header before first extension
            if needs_header:
                claude_md_content = claude_md_content.rstrip() + "\n\n## Project-Specific Extensions\n"
                needs_header = False

            # Append extension content
            append_content = append_file.read_text()
            claude_md_content += f"\n{append_content}"
            claude_md_path.write_text(claude_md_content)

        # Update extensions.json
        installed.append(ext_name)
        save_extensions_file({"extensions": installed}, project_dir)

        print(f"Added extension '{ext_name}'")


def cmd_init(args):
    """Create a new project with base template and optional extensions."""
    project_name = args.project_name

    # Handle "." as current directory
    if project_name == ".":
        project_path = Path.cwd()
        is_current_dir = True
    else:
        project_path = Path.cwd() / project_name
        is_current_dir = False

        # Validate project name (only for new directories, not ".")
        if "/" in project_name or "\\" in project_name or project_name.startswith("."):
            die(f"Invalid project name '{project_name}'")

    if project_path.exists():
        # Check if already a cframe project
        if (project_path / ".claude" / "extensions.json").exists():
            die(f"Directory is already a cframe project")

        # Check for existing Claude files
        has_claude_dir = (project_path / ".claude").exists()
        has_claude_md = (project_path / "CLAUDE.md").exists()
        if has_claude_dir or has_claude_md:
            die("Directory already contains Claude files (.claude/ or CLAUDE.md)\nRemove these files first or use a different directory.")
        is_existing_dir = True
    else:
        # Create new project directory
        project_path.mkdir()
        is_existing_dir = False

    # Copy base template
    base_template = get_template_dir() / "base"
    copy_directory(base_template, project_path)

    if is_current_dir:
        print("Initialized cframe project in current directory")
    elif is_existing_dir:
        print(f"Initialized cframe project in '{project_name}'")
    else:
        print(f"Created project '{project_name}'")

    # Apply extensions if specified
    if hasattr(args, "extensions") and args.extensions:
        apply_extensions(args.extensions, project_path)


def cmd_add(args):
    """Add extensions to an existing project."""
    if not is_valid_project():
        die("Not a valid cframe project (missing .claude/extensions.json)")

    if not args.extensions:
        die("No extensions specified. Use --<extension> flags.\nRun 'cframe list' to see available extensions.")

    apply_extensions(args.extensions, Path.cwd())


def cmd_list(args):
    """List all available extensions."""
    registry = get_registry()
    extensions = registry.get("extensions", {})

    if not extensions:
        print("No extensions available.")
        return

    print("Available extensions:\n")
    for name, description in extensions.items():
        print(f"  --{name:<12} {description}")


def cmd_status(args):
    """Show installed and available extensions for current project."""
    if not is_valid_project():
        die("Not a valid cframe project (missing .claude/extensions.json)")

    registry = get_registry()
    available = set(registry.get("extensions", {}).keys())
    installed = set(get_extensions_file().get("extensions", []))
    not_installed = available - installed

    print("Installed:")
    if installed:
        for name in sorted(installed):
            print(f"  {name}")
    else:
        print("  (none)")

    print("\nAvailable:")
    if not_installed:
        for name in sorted(not_installed):
            print(f"  --{name}")
    else:
        print("  (all extensions installed)")


def add_extension_flags(parser) -> None:
    """Add extension flags to a parser based on registry."""
    registry = get_registry()
    for name, description in registry.get("extensions", {}).items():
        parser.add_argument(
            f"--{name}",
            action="append_const",
            const=name,
            dest="extensions",
            help=description,
        )


def main():
    parser = argparse.ArgumentParser(
        prog="cframe",
        description="Initialize and manage Claude-based project structures",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # init command
    init_parser = subparsers.add_parser(
        "init", help="Create a new project from base template"
    )
    init_parser.add_argument(
        "project_name", help="Name of the project directory to create"
    )
    add_extension_flags(init_parser)
    init_parser.set_defaults(func=cmd_init)

    # add command
    add_parser = subparsers.add_parser(
        "add", help="Add extensions to the current project"
    )
    add_extension_flags(add_parser)
    add_parser.set_defaults(func=cmd_add)

    # list command
    list_parser = subparsers.add_parser(
        "list", help="List all available extensions"
    )
    list_parser.set_defaults(func=cmd_list)

    # status command
    status_parser = subparsers.add_parser(
        "status", help="Show installed and available extensions"
    )
    status_parser.set_defaults(func=cmd_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
