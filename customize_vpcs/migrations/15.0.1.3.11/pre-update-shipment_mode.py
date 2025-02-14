def migrate(cr, version):
    """Update the table
    Set the shipment mode to the lowest id of the shipment mode with the same name
    """
    cr.execute(
        """UPDATE project_project prj
            SET mode_shipment_air_sea = (
                SELECT MIN(t1.id)
                FROM mode_shipment t1
                WHERE t1.name = (SELECT name FROM mode_shipment ms WHERE ms.id = prj.mode_shipment_air_sea)
            )
            WHERE EXISTS (
                SELECT 1
                FROM mode_shipment ms
                WHERE ms.id = prj.mode_shipment_air_sea
                AND ms.id > (SELECT MIN(t1.id) FROM mode_shipment t1 WHERE t1.name = ms.name)
            );
        """
    )
