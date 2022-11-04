# Nutshell

a lecture note-writing app, with automatic questionnaire generation

## INSTALL

install chocolatey (run in admin powershell):

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

then (admin powershell):

```
choco install ffmpeg
```

create virtual environment:
(and then activate the new environment)

```
python -m venv .venv
```

install packages:

```
pip install -r requirements.txt
```
