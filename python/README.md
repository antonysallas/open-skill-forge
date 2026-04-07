# Python Environment

## Prerequisites

- **macOS/Linux:** `curl` and a POSIX shell
- **Windows:** PowerShell 5.1+

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
1. Install JupyterLab via uv
1. Clone the repository to `~/open-skill-forge/`
1. Launch JupyterLab in the notebooks directory

## Uninstall

### macOS / Linux (Uninstall)

```bash
curl -LsSf https://raw.githubusercontent.com/antonysallas/open-skill-forge/main/python/setup/remove.sh | bash
```

### Windows (Uninstall)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://raw.githubusercontent.com/antonysallas/open-skill-forge/main/python/setup/remove.ps1 | iex"
```

To skip the confirmation prompt (e.g. in CI), pass the force flag:

```bash
bash python/setup/remove.sh --force
```

```powershell
.\python\setup\remove.ps1 -Force
```

The removal script will:

1. Uninstall JupyterLab
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
