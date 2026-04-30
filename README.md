# 2526-unibe-music-player
This repository maintains the code for the Advanced Python 2026 Project.
##### The group members are Andri Widmer, Andy Nkunzimana, Mario Amos and Rohit Bharatia.
The project aims to create a Music player in 3 stages:
1. IO management and database creation.
2. Integration of DB search for users as well as addition of amplification and scrubbing features.
3. Implementation of actual playback through system hardware and visualiser.  

#### Project Overview
The project uses Python for the entirety of the codebase. The packages used are listed in the pyproject.toml file. They are grouped in
functional and developer packages. The package manager used for this project is uv. If you do not have uv please install it.
#### UV Installation.
For Linux/macOS
```bash
curl -sSf https://install.astral.sh/uv | sh
```
If you do not have curl use:
```bash
wget -qO- https://install.astral.sh/uv | sh
```
Alternatively it can be installed using pip
```bash
pip install uv
```
For windows:
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
If you already have an uv installation you can update it if required using 
```bash
uv self update
```
Additional methods and extensive documentation can be found at the following link https://docs.astral.sh/uv/getting-started/installation/

### Installation guide
##### Clone project 
Using SSH (recommended)
```bash
git clone git@github.com:python-data-science-2026/2526-unibe-music-player.git
```
Using HTTPS(deprecated and not recommended)
```bash
git clone https://github.com/python-data-science-2026/2526-unibe-music-player.git
```
##### Environment Set-up
Change into your git tracked directory
```bash
cd ./2526-unibe-music-player
```
```bash
uv sync
```
If you would not like to install the extra developer packages use
```bash
uv sync --no-dev
```

## Running the project
To run the project ensure you are in the src directory and then:
```bash
uv run main.py
```

