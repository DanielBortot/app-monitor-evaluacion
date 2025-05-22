<div align="center">
  <img src="./public/images/icons/Python-logo-notext.svg.png" width="200" alt="Unity Logo" />
</div>

# Evaluation Monitoring Scripts

This repository contains the Scripts of Steam Monitoring in diferent os

## Requirements

- Python

## Installation

1. Clone the project on your computer:

   ```bash
   git clone https://github.com/DanielBortot/app-monitor-evaluacion1
   ```

2. Create the Python virtual environment

   ```bash
   # Run the following command to create a virtual environment in the project directory:
   python -m venv venv
   ```

3. Activate the virtual environment

   ```bash
   # Windows (using Command Prompt):
   venv\Scripts\activate

   # Windows (using PowerShell):
   .\venv\Scripts\activate.ps1

   # macOS and Linux:
   source venv/bin/activate
   ```

4. Install the dependencies

   ```bash
   # Run the following command:
   pip install -r requirements.txt
   ```

5. Update dependencies

   ```bash
   # Run the following command to update the requirements file:
   pip freeze > requirements.txt
   ```

6. Run the Scripts

```bash
   #Run it in Windows
   python .\app_monitor_windows.py
   #Run it in Linux
   python .\app_monitor_Linux.py
```

```bash
# It appears something like this
(venv) PS C:\your-path> python .\app_monitor_windows.py
Ingresa el nombre de la aplicacion o proceso: steam
Ingrese la cantidad de registros que quiere realizar (cada registro toma un segundo): 100

 ```

## Contributions

<table align="center">
    <tbody>
        <tr>
            <td align="center">
                <a href="https://github.com/Fussita" rel="nofollow">
                    <img src="https://avatars.githubusercontent.com/u/110612202?v=4" width="150px;" alt="" style="max-width:100%;">
                    <br>
                    <sub><b>Hualong Chiang</b></sub>
                </a>
                <br>
                <a href="" title="Commits">
                    <g-emoji class="g-emoji" alias="book" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f4d6.png">📖</g-emoji>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/C102002" rel="nofollow">
                    <img src="https://avatars.githubusercontent.com/u/116277334?v=4" width="150px;" alt="" style="max-width:100%;">
                    <br>
                    <sub><b>Alfredo Fung</b></sub>
                </a>
                <br>
                <a href="" title="Commits">
                    <g-emoji class="g-emoji" alias="book" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f4d6.png">📖</g-emoji>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/DanielBortot" rel="nofollow">
                    <img src="https://avatars.githubusercontent.com/u/103535845?v=4" width="150px;" alt="" style="max-width:100%;">
                    <br>
                    <sub><b>Daniel Bortot</b></sub>
                </a>
                <br>
                <a href="" title="Commits">
                    <g-emoji class="g-emoji" alias="book" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f4d6.png">📖</g-emoji>
                </a>
            </td>
        </tr>
    </tbody>
</table>

## License

This project is under Apache license. See the [LICENSE](LICENSE) file for more details.
