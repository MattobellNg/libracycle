def migrate(cr, version):
    cr.execute("ALTER TABLE project_project ADD COLUMN temporary_kg int")
    cr.execute("ALTER TABLE project_project ADD COLUMN temporary_cbm int")
    cr.execute("ALTER TABLE project_project ADD COLUMN temporary_mode_shipment_air_sea int")

    # Update the table
    cr.execute("UPDATE project_project SET temporary_kg = kg")
    cr.execute("UPDATE project_project SET temporary_cbm = cbm")
    cr.execute("UPDATE project_project SET temporary_mode_shipment_air_sea = (SELECT mode_shipment_id from mode_shipment_project_project_rel where project_project_id = id limit 1)")
