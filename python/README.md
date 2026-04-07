# Python Environment

## Prerequisites

- **macOS/Linux:** `curl`, `git`, and a POSIX shell
- **Windows:** PowerShell 5.1+ and `git`

## One Script Install (Recommended)

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

## Manual Install (Fallback)

If the setup script doesn't work, run these commands directly.

### macOS / Linux (Manual)

```bash
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.local/bin/env

# 2. Install Python
uv python install 3.12

# 3. Clone the repo
mkdir -p ~/projects
git clone https://github.com/antonysallas/open-skill-forge.git \
  ~/projects/open-skill-forge

# 4. Create venv and install JupyterLab
uv venv --python 3.12 ~/projects/open-skill-forge/.venv
source ~/projects/open-skill-forge/.venv/bin/activate
uv pip install jupyterlab

# 5. Launch
cd ~/projects/open-skill-forge/python/notebooks
jupyter lab
```

### Windows (Manual)

```powershell
# 1. Install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Install Python
uv python install 3.12

# 3. Clone the repo
New-Item -ItemType Directory -Path "$env:USERPROFILE\projects" -Force
git clone https://github.com/antonysallas/open-skill-forge.git `
  "$env:USERPROFILE\projects\open-skill-forge"

# 4. Create venv and install JupyterLab
uv venv --python 3.12 "$env:USERPROFILE\projects\open-skill-forge\.venv"
& "$env:USERPROFILE\projects\open-skill-forge\.venv\Scripts\Activate.ps1"
uv pip install jupyterlab

# 5. Launch
cd "$env:USERPROFILE\projects\open-skill-forge\python\notebooks"
jupyter lab
```

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
