import pandas as pd

from etl.services.excel_reader import (
    FILE_PATH,
    TRANFS_MAPPING,
    read_excel_with_mapping
)

# ======================================================
# PRIORIDAD DE ESTATUS
# ======================================================
STATUS_PRIORITY = {
    "TRANSITO": 1,
    "YARDA": 2,
    "RECEIVING": 3,
}

# ======================================================
# ESQUEMA ESTÁNDAR DEL INVENTARIO
# ======================================================
STANDARD_COLUMNS = [
    "cutting",
    "zr",
    "order_type",
    "contenedor",
    "swo",
    "aging_days",
    "cb",
    "item",
    "status",
    "units",
    "location",
    "style",
    "swo_style",
    "color",
    "size",
]

# ======================================================
# NORMALIZAR DATAFRAME
# ======================================================
def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    for col in STANDARD_COLUMNS:
        if col not in df.columns:
            df[col] = None
    return df[STANDARD_COLUMNS]

# ======================================================
# CARGAR DATA DESDE EXCEL
# ======================================================
def load_inventory_from_excel() -> pd.DataFrame:
    """
    Lee las hojas del inventario y devuelve
    un DataFrame consolidado por CUTTING
    """

    # -------- TRÁNSITO --------
    df_transito = read_excel_with_mapping(
        file_path=FILE_PATH,
        sheet_name="DCBTRANFS1",
        mapping=TRANFS_MAPPING,
        fixed_values={
            "status": "TRANSITO",
            "location": "TRANSITO",
        }
    )

    # -------- YARDA --------
    df_yarda = read_excel_with_mapping(
        file_path=FILE_PATH,
        sheet_name="DCBYARDZR5",
        mapping={
            "LILOTN": "cutting",
            "IMLITM": "cb",
            "LIPQOH": "units",
            "IMSRP101": "style",
            "IMSRP201": "color",
            "IMSRP301": "size",
            "PHDOCO": "zr",
            "PHDCTO": "order_type",
            "IOLOT1": "contenedor",
        },
        fixed_values={
            "status": "YARDA",
            "location": "YARDA",
        }
    )

    # -------- RECEIVING --------
    df_receiving = read_excel_with_mapping(
        file_path=FILE_PATH,
        sheet_name="DCBHAND2",
        mapping={
            "PDDSC1": "cutting",
            "PDLITM": "cb",
            "PDUOPN": "units",
            "IMSRP101": "style",
            "IMSRP201": "color",
            "IMSRP301": "size",
            "PDLOCN": "location",  # RCVG01 / RCVG02
        },
        fixed_values={
            "status": "RECEIVING",
        }
    )

    # -------- UNIFICAR --------
    df_all = pd.concat(
        [df_transito, df_yarda, df_receiving],
        ignore_index=True
    )

    # -------- NORMALIZAR --------
    df_all = normalize_dataframe(df_all)

    # -------- PRIORIZAR ESTATUS --------
    df_all["status_rank"] = df_all["status"].map(STATUS_PRIORITY)

    df_final = (
        df_all.sort_values("status_rank")
              .groupby("cutting", as_index=False)
              .last()
    )

    df_final = df_final.drop(columns=["status_rank"])

    return df_final
