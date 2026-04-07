# Python Environment

## Prerequisites

- **macOS/Linux:** `curl` and a POSIX shell
- **Windows:** PowerShell 5.1+

## Install

### macOS / Linux

```bash
bash python/setup/setup.sh
```

### Windows

```powershell
.\python\setup\setup.ps1
```

The setup script will:

1. Install [uv](https://docs.astral.sh/uv/) (skipped if already installed)
1. Install Python 3.12 via uv
1. Install JupyterLab via uv

Once complete, start JupyterLab with:

```bash
jupyter lab
```

## Uninstall

### macOS / Linux (Uninstall)

```bash
bash python/setup/remove.sh
```

### Windows (Uninstall)

```powershell
.\python\setup\remove.ps1
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
