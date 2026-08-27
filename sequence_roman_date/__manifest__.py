{
    'name': 'Sequence Roman Date',
    'version': '19.0.1.0.0',
    'category': 'Technical Settings',
    'summary': 'Add Roman Numeral Legend (Month & Year) to Sequences',
    'description': """
Roman Numerals for Odoo Sequences
=================================
Tired of standard numeric dates in your sequences? 
This module allows you to use Roman Numerals for Month and Year in Odoo Sequences.

Perfect for companies requiring unique document formatting (e.g., invoices, internal memos, or legal documents) using Month (I-XII) and Year (Roman format).

Key Features:
-------------
*   **%(month_roman)s**: Use Roman numerals for Month (I, II, III ... XII).
*   **%(year_roman)s**: Use Roman numerals for Year (e.g., 2024 -> MMXXIV).
*   Lightweight & no complex configurations.
*   Preserves all standard Odoo sequence legends.
    """,
    'author': 'hamzbond',
    'website': 'https://hamzbond.github.io',
    'license': 'LGPL-3',
    'price': 0.00,
    'currency': 'EUR',
    'images': ['static/description/banner.png'],
    'depends': ['base'],
    'data': [
        'views/ir_sequence_views.xml',
    ],
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
    'auto_install': False,
    'application': False,
}
