from . import models

def uninstall_hook(cr, registry):
    cr.execute("""
        UPDATE ir_sequence
        SET prefix = REPLACE(prefix, '%(month_roman)s', ''),
            suffix = REPLACE(suffix, '%(month_roman)s', '')
        WHERE prefix LIKE '%%(month_roman)s%%' OR suffix LIKE '%%(month_roman)s%%'
    """)
    cr.execute("""
        UPDATE ir_sequence
        SET prefix = REPLACE(prefix, '%(year_roman)s', ''),
            suffix = REPLACE(suffix, '%(year_roman)s', '')
        WHERE prefix LIKE '%%(year_roman)s%%' OR suffix LIKE '%%(year_roman)s%%'
    """)