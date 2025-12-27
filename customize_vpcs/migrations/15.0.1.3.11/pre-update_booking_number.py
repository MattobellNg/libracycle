def migrate(cr, version):
    # Update the table
    cr.execute("ALTER TABLE project_project DROP COLUMN booking_number;")
