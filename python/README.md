# Python Environment

## Prerequisites

- **macOS/Linux:** `curl`, `git`, and a POSIX shell
- **Windows:** PowerShell 5.1+ and `git`

## Install

### macOS / Linux

```bash
curl -LsSf https://raw.githubusercontent.com/antonysallas/open-skill-forge/main/python/setup/setup.sh | bash
```

### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/antonysallas/open-skill-forge/main/python/setup/setup.ps1 | iex"
```

The setup script will:

1. Install [uv](https://docs.astral.sh/uv/) (skipped if already installed)
1. Install Python 3.12 via uv
1. Clone the repository to `~/projects/open-skill-forge/`
1. Create a virtual environment in the project directory
1. Install JupyterLab in the virtual environment

Then follow the printed instructions to start JupyterLab.

## Uninstall

From the cloned repository (`~/projects/open-skill-forge/`):

### macOS / Linux (Uninstall)

```bash
bash ~/projects/open-skill-forge/python/setup/remove.sh
```

### Windows (Uninstall)

```powershell
& "$env:USERPROFILE\projects\open-skill-forge\python\setup\remove.ps1"
```

To skip the confirmation prompt (e.g. in CI):

```bash
bash python/setup/remove.sh --force
```

```powershell
.\python\setup\remove.ps1 -Force
```

The removal script will:

1. Remove the cloned repository and virtual environment
1. Remove all uv-managed Python installations
1. Remove uv and its data/cache directories

## Directory Structure

```text
python/
├── README.md
├── notebooks/          # Jupyter notebooks
│   └── 01_zen_of_python.ipynb
└── setup/
    ├── setup.sh        # Install (macOS/Linux)
    ├── setup.ps1       # Install (Windows)
    ├── remove.sh       # Uninstall (macOS/Linux)
    └── remove.ps1      # Uninstall (Windows)
```
