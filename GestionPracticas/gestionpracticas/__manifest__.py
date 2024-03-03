# -*- coding: utf-8 -*-
{
    'name': "gestionpracticas",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reports/report_profesores.xml',
        'reports/report_profesores_alumnos.xml',
        'reports/report_ciclos_formativos.xml',
        'reports/report_ciclos_formativos_coordinadores.xml',
        'reports/report_ciclos_formativos_profesores.xml',
        'reports/report_alumnos.xml',
        'reports/report_empresas.xml',
        'reports/report_practicas_empresas.xml',
        'data/data.xml',
    #    'data/email_template.xml',
    ],

    # Add the 'images' key to specify the icon for your module
    'images': ['static/description/icon.png'],

    'application': True,

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
