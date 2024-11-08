#maak de virtuele omgeving
python -m venv .venv
# activeer de vrituele omgeving
$venvPath = ".venv\Scripts\Activate"
& $venvPath
# Eventueel extra commando's die je binnen de omgeving wilt uitvoeren:
pip install -r requirements.txt
