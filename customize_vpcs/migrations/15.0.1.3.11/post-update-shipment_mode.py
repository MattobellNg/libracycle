def migrate(cr, version):
    """Update the table
    Delete all the shipment mode with the same name except the one with the lowest id.
    """
    cr.execute(
        """DELETE FROM mode_shipment WHERE id NOT IN (
            SELECT MIN(id)
            FROM mode_shipment
            GROUP BY name
        );"""
    )