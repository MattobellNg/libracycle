def migrate(cr, version):
    # Update the table
    cr.execute("UPDATE project_project DROP COLUMN booking_number")
