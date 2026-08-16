"""
14_antigravity_state_consolidation.py
Consolidation script to resolve state fragmentation for Antigravity.
Issue: INV-11 (P0 Consolidar estado dividido entre C:\\Users\\Lenovo\\ANTIGRAVITY_CORE y D:\\.gemini_storage)

This script acts as a dry-run auditor and migrator to consolidate annotations,
oauth_creds.json, and config files from D:\\.gemini_storage into the active runtime
path C:\\Users\\Lenovo\\ANTIGRAVITY_CORE without losing credentials.
"""

import os
import sys
import shutil
import json
from pathlib import Path

# Paths based on INV-11 report
SOURCE_DIR = Path("D:/.gemini_storage")
TARGET_DIR = Path("C:/Users/Lenovo/ANTIGRAVITY_CORE")

# Mock paths for Linux execution (testing/verification)
if sys.platform != "win32":
    SOURCE_DIR = Path("/tmp/mock_gemini_storage")
    TARGET_DIR = Path("/tmp/mock_antigravity_core")

CRITICAL_FILES = [
    "oauth_creds.json",
    "configs.json",
    "annotations/",
    "antigravity/"
]

def create_mock_environment():
    """Create mock files on Linux so the script can be tested safely."""
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    with open(SOURCE_DIR / "oauth_creds.json", "w", encoding="utf-8") as f:
        json.dump({"client_id": "MOCK_CLIENT_ID_123"}, f)

    (SOURCE_DIR / "annotations").mkdir(parents=True, exist_ok=True)
    with open(SOURCE_DIR / "annotations" / "state.txt", "w", encoding="utf-8") as f:
        f.write("fragmented state data")

def audit_fragmentation() -> list:
    """Inventories missing or fragmented files between Source and Target."""
    print(f"=== INICIANDO AUDITORIA DE FRAGMENTACION ===")
    print(f"Fuente (Storage): {SOURCE_DIR}")
    print(f"Destino (Runtime): {TARGET_DIR}\n")

    actions_needed = []

    if not SOURCE_DIR.exists():
        print(f"[!] Directorio fuente {SOURCE_DIR} no encontrado. No hay nada que consolidar.")
        return actions_needed

    for item_name in CRITICAL_FILES:
        source_path = SOURCE_DIR / item_name.strip("/")
        target_path = TARGET_DIR / item_name.strip("/")

        if source_path.exists():
            if not target_path.exists():
                print(f"[REQUERIDO] {item_name} existe en Storage pero NO en Runtime.")
                actions_needed.append((source_path, target_path))
            else:
                print(f"[CONFLICTO] {item_name} existe en AMBOS directorios. Se requiere resolucion manual de merge.")
        else:
            print(f"[OK] {item_name} no está en Storage.")

    return actions_needed

def execute_consolidation(actions: list, dry_run: bool = True):
    """Executes the safe migration of files."""
    print("\n=== EJECUTANDO CONSOLIDACION ===")
    if dry_run:
        print("[MODO DRY-RUN ACTIVADO: No se modificaran archivos]")

    for src, dst in actions:
        print(f"-> Moviendo: {src} ===> {dst}")
        if not dry_run:
            try:
                # Si es un archivo, copia preservando metadata
                if src.is_file():
                    shutil.copy2(src, dst)
                # Si es un directorio, copia el arbol
                elif src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                print(f"   [EXITO] Movimiento completado.")
            except Exception as e:
                print(f"   [ERROR] Fallo al mover {src}: {e}")

def main():
    # Solo para testing automatizado en el CI/VM
    if sys.platform != "win32":
        create_mock_environment()

    actions = audit_fragmentation()

    if actions:
        execute_consolidation(actions, dry_run=True)
        print("\nPara ejecutar la consolidacion real, cambia dry_run=False en el script.")
    else:
        print("\nEl estado está completamente consolidado. No hay acciones pendientes.")

if __name__ == "__main__":
    main()
