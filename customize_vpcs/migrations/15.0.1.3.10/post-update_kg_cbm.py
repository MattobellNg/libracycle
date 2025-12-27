def migrate(cr, version):
    # Update the table
    cr.execute("UPDATE project_project SET kg = temporary_kg;")
    cr.execute("UPDATE project_project SET cbm = temporary_cbm;")
    cr.execute("UPDATE project_project SET mode_shipment_air_sea = temporary_mode_shipment_air_sea;")

    # Alter the table
    cr.execute("ALTER TABLE project_project DROP COLUMN temporary_kg;")
    cr.execute("ALTER TABLE project_project DROP COLUMN temporary_cbm;")
    cr.execute("ALTER TABLE project_project DROP COLUMN temporary_mode_shipment_air_sea;")
    cr.execute("DROP TABLE mode_shipment_project_project_rel;")
