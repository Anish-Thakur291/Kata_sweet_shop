Run Django `manage.py` from this folder

You can run Django management commands from inside the `api` folder using one of these helpers:

- PowerShell: `run_manage.ps1`
- Windows CMD: `run_manage.bat`
- Python: `manage_proxy.py`

Examples (PowerShell):

```powershell
# run makemigrations
.\run_manage.ps1 makemigrations

# apply migrations
.\run_manage.ps1 migrate
```
