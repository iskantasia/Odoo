# -*- coding: utf-8 -*-
{
    'name': "Purchase Bayu",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "PT. Jababeka & Co",
    'website': "https://www.jababeka.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'purchase',
        'product'
        # 'base64'
    ],

    # always loaded
    'data': [
        'security/role.xml',
        'security/ir.model.access.csv',
        'views/sequence.xml',
        'views/sequence1.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/report.xml'
    #   'views/purchasing_menu.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    # 'external_dependencies': {
    #   'python': ['ldap3'],
    # },
    # 'sequence': 2,
    # 'auto_install': False,
    # 'installable': True,
    # 'application': True,

}
