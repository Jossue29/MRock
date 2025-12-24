import pandas as pd
from django.conf import settings
import os

# ======================================================
# Ruta fija del archivo Excel (QGPL refresh)
# ======================================================
FILE_PATH = os.path.join(
    settings.MEDIA_ROOT,
    "Excel",
    "raw",
    "Inventario.xlsm"
)

# ======================================================
# MAPPING TRÁNSITO (DCBTRANFS1)
# ======================================================
TRANFS_MAPPING = {
    "PDDSC1": "cutting",
    "PDDOCO": "zr",
    "PDDCTO": "order_type",
    "PDVR02": "contenedor",
    "PDLITM": "cb",
    "PDUOPN": "units",
    "IMSRP101": "style",
    "IMSRP201": "color",
    "IMSRP301": "size",
}

# ======================================================
# FUNCIÓN GENÉRICA DE LECTURA
# ======================================================
def read_excel_with_mapping(
    file_path: str,
    sheet_name: str,
    mapping: dict,
    fixed_values: dict = None
):
    print("📄 FILE_PATH =", file_path)

    df = pd.read_excel(file_path, sheet_name=sheet_name)
    print("📊 Columnas originales:", df.columns.tolist())

    # Renombrar columnas según mapping
    df = df.rename(columns=mapping)

    for col in mapping.values():
        if col not in df.columns:
         df[col] = None

    df = df[list(mapping.values())]


    # Agregar columnas fijas (status, location, etc.)
    if fixed_values:
        for col, value in fixed_values.items():
            df[col] = value

    return df
