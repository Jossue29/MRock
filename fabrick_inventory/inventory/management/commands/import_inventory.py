from django.core.management.base import BaseCommand
from django.db import transaction

from inventory.models import GlobalInventory, InventoryHistory
from etl.services.inventory_transformer import load_inventory_from_excel

def safe_int(value):
    try:
        if value is None:
            return None
        if isinstance(value, float) and value != value:  # NaN
            return None
        return int(value)
    except (ValueError, TypeError):
        return None


class Command(BaseCommand):
    help = "Import inventory and track history"

    def handle(self, *args, **options):
        df = load_inventory_from_excel()

        created = 0
        updated = 0
        history_events = 0
        skipped = 0

        for _, row in df.iterrows():
            cutting = safe_int(row.get("cutting"))

            if not cutting:
                skipped += 1
                continue

            defaults = {
                "zr": row.get("zr"),
                "order_type": (row.get("order_type")),
                "contenedor": (row.get("contenedor")),
                "swo": safe_int(row.get("swo")),
                "aging_days": safe_int(row.get("aging_days")),
                "cb": (row.get("cb")),
                "item": (row.get("item")) or "",
                "status": (row.get("status")),
                "location": (row.get("location")),
                "units": safe_int(row.get("units")) or 0,
                "style": (row.get("style")),
                "swo_style": (row.get("swo_style")),
                "color": (row.get("color")),
                "size": (row.get("size")),
                "source_report": (row.get("source_report")) or "IMPORT",
            }

            with transaction.atomic():
                inv = GlobalInventory.objects.filter(cutting=cutting).first()

                # ───────── NUEVO ─────────
                if not inv:
                    inv = GlobalInventory.objects.create(
                        cutting=cutting,
                        **defaults
                    )

                    InventoryHistory.objects.create(
                        cutting=cutting,
                        previous_status=None,
                        previous_location=None,
                        previous_units=None,
                        previous_contenedor=None,
                        new_status=inv.status,
                        new_location=inv.location,
                        new_units=inv.units,
                        new_contenedor=inv.contenedor,
                        source_report=inv.source_report,
                        event_type="CREATED"
                    )

                    created += 1
                    history_events += 1
                    continue

                # ─────── EXISTENTE ───────
                has_change = (
                    inv.status != defaults["status"]
                    or inv.location != defaults["location"]
                    or inv.units != defaults["units"]
                    or inv.contenedor != defaults["contenedor"]
                )

                if has_change:
                    InventoryHistory.objects.create(
                        cutting=cutting,
                        previous_status=inv.status,
                        previous_location=inv.location,
                        previous_units=inv.units,
                        previous_contenedor=inv.contenedor,
                        new_status=defaults["status"],
                        new_location=defaults["location"],
                        new_units=defaults["units"],
                        new_contenedor=defaults["contenedor"],
                        source_report=defaults["source_report"],
                        event_type=f"{inv.status}→{defaults['status']}"
                    )

                    for field, value in defaults.items():
                        setattr(inv, field, value)

                    inv.save()
                    updated += 1
                    history_events += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✔ Import terminado | creados={created} | "
                f"actualizados={updated} | eventos={history_events} | "
                f"omitidos={skipped}"
            )
        )
