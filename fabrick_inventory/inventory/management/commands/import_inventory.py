from django.core.management.base import BaseCommand
from etl.services.inventory_transformer import load_inventory_from_excel

class Command(BaseCommand):
    help = "Importa inventario desde Excel"

    def handle(self, *args, **options):
        df = load_inventory_from_excel()

        self.stdout.write(
            self.style.SUCCESS(
                f"Inventario cargado correctamente. Registros: {len(df)}"
            )
        )
