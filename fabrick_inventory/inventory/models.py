from django.db import models

class GlobalInventory(models.Model):
    # === Identificador principal ===
    cutting = models.BigIntegerField(
        unique=True,
        db_index=True,
        verbose_name="Cutting Number"
    )

    # === Datos de orden / logística ===
    zr = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    order_type = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    contenedor = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    swo = models.BigIntegerField(
        null=True,
        blank=True
    )

    # === Aging / antigüedad ===
    aging_days = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # === Item / material ===
    cb = models.CharField(
        max_length=30
    )

    item = models.BigIntegerField()

    # === Estatus y ubicación ===
    status = models.CharField(
        max_length=20,
        db_index=True
    )

    location = models.CharField(
        max_length=20,
        db_index=True
    )

    # === Cantidades ===
    units = models.PositiveIntegerField()

    # === Atributos de producto ===
    style = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    swo_style = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    color = models.CharField(
        max_length=30
    )

    size = models.CharField(
        max_length=30
    )

    # === Control del sistema ===
    source_report = models.CharField(
        max_length=30,
        help_text="Reporte que originó el último update"
    )

    last_updated = models.DateTimeField(
        auto_now=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "global_inventory"
        verbose_name = "Global Inventory"
        verbose_name_plural = "Global Inventories"

    def __str__(self):
        return f"Cutting {self.cutting} - {self.status}"
