import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent))

from src.gui import main

if __name__ == '__main__':
    main() 