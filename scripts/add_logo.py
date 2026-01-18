#!/usr/bin/env python3
"""
Script pour ajouter le logo TauIA à l'application.

Usage:
    python scripts/add_logo.py /path/to/tauia_logo.png
"""

import sys
import shutil
from pathlib import Path

def add_logo(source_path: str):
    """Copie le logo dans le dossier assets."""
    source = Path(source_path)

    if not source.exists():
        print(f"❌ Erreur: Le fichier {source_path} n'existe pas")
        return False

    if source.suffix.lower() not in ['.png', '.jpg', '.jpeg', '.svg']:
        print(f"⚠️  Attention: Format {source.suffix} non optimal. PNG recommandé.")

    # Créer le dossier assets si nécessaire
    assets_dir = Path(__file__).parent.parent / "assets"
    assets_dir.mkdir(exist_ok=True)

    # Copier le fichier
    dest = assets_dir / "logo.png"
    shutil.copy2(source, dest)

    print(f"✅ Logo copié avec succès dans {dest}")
    print(f"📏 Taille: {dest.stat().st_size / 1024:.1f} KB")
    print("\n🚀 Relancer l'application pour voir le logo:")
    print("   streamlit run app.py")

    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/add_logo.py /path/to/logo.png")
        sys.exit(1)

    add_logo(sys.argv[1])
