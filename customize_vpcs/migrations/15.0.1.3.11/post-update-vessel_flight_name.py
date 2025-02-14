def migrate(cr, version):
    # copy values saved in the temporary columns to the real columns
    cr.execute("UPDATE project_project SET ves_line = temporary_ves_line;")
  
    # drop the temporary columns
    cr.execute("ALTER TABLE project_project DROP COLUMN temporary_ves_line;")
