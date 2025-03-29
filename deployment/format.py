import json
import sys

with open(sys.argv[1], 'r') as f:
    content = f.read()

cleaned_content = content.replace('\n', '').strip()

try:
    data = json.loads(cleaned_content)
    
    with open(sys.argv[1], 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Fichier JSON reformaté avec succès.")
except json.JSONDecodeError as e:
    print(f"Erreur de décodage JSON : {e}")
    sys.exit(1)