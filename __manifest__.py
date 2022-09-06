# -*- coding: utf-8 -*-
{
    'name': "icc_anal_base",

    'summary': """
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail',],

    # always loaded
    'data': [
        'security/group_task.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/cle_repartition.xml',
        'views/equipement.xml',
        'views/devise.xml',
        'views/devis1.xml',
        'views/compte_exploi.xml',
        'views/submit.xml',
        'views/critere_eva.xml',
        'views/critere.xml',
        'views/notation.xml',
        'views/notation_equip.xml',
        'views/grille_critere.xml',
        'views/anal_project.xml',
        'views/parametre.xml',
        'menu.xml',
        'views/login.xml',
        'reports/compte_report.xml',
        'reports/devis_estimatif.xml',
        'reports/report.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
