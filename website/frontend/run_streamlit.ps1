# Helper script to run the Streamlit app using the workspace Python interpreter
# Usage: Right-click -> Run with PowerShell, or execute from PowerShell:
#   .\run_streamlit.ps1

$python = 'C:/Users/antec/AppData/Local/Python/pythoncore-3.14-64/python.exe'
Set-Location -Path "e:\DEPI\Technical\final\Final_project\website\frontend"
& $python -m streamlit run streamlit_test_app.py
