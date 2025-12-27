def migrate(cr, version):

    # Add a temporary column to store the vessel fligth name
    cr.execute("ALTER TABLE project_project ADD COLUMN temporary_ves_line char(64)")

    # Copy the text value of the vessel flight name to the temporary column
    cr.execute("UPDATE project_project SET temporary_ves_line = (SELECT name FROM vessel_line WHERE id = ves_line);")
    
