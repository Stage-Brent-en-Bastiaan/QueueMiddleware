# Pad naar de virtuele omgeving
$venvPath = "venv\Scripts\Activate"

# Activeer de virtuele omgeving
& $venvPath

# Eventueel extra commando's die je binnen de omgeving wilt uitvoeren:
python --version

pip install -r requirements.txt
