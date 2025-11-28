#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import List
import argostranslate.package as pkg
import argostranslate.translate as argo

MAX_LEN = 100000
FROM = "es"
TO = "pt"

def ensure_model(from_code: str, to_code: str) -> None:
    """
    Instala el paquete de traducción si no está ya instalado.
    Descarga desde el índice oficial de Argos Translate.
    """
    installed = pkg.get_installed_packages()
    for p in installed:
        if p.from_code == from_code and p.to_code == to_code:
            return  # ya está

    # No está instalado: buscarlo y descargarlo
    pkg.update_package_index()
    available: List[pkg.Package] = pkg.get_available_packages()
    candidates = [p for p in available if p.from_code == from_code and p.to_code == to_code]
    if not candidates:
        raise RuntimeError(f"No hay modelo {from_code}->{to_code} disponible en el índice.")
    # coge el primero (suele ser el único)
    package = candidates[0]
    path = package.download()         # descarga .argosmodel
    pkg.install_from_path(path)       # instala

def translate_es_to_pt(text: str) -> str:
    ensure_model(FROM, TO)
    return argo.translate(text, FROM, TO)

def main():
    if len(sys.argv) <= 1:
        print("Uso: python translate.py \"texto en español\"", file=sys.stderr)
        sys.exit(1)

    text = " ".join(sys.argv[1:]).strip()
    if not text:
        print("Error: texto vacío.", file=sys.stderr); sys.exit(1)
    if len(text) > MAX_LEN:
        print(f"Error: máximo {MAX_LEN} caracteres (recibidos {len(text)}).", file=sys.stderr)
        sys.exit(1)

    try:
        print(translate_es_to_pt(text))
    except Exception as e:
        print(f"Error de traducción: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
