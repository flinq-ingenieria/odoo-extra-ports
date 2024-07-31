# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Attendance reminder',
    'version': '15.0.1.0.0',
    'summary': '',
    'category': 'Human Resources',
    'author': 'zvERP.com, comunitea',
    'maintainer': 'zvERP.com',
    'website': 'www.zverp.com',
    'license': 'AGPL-3',
    'depends': [
        'hr_attendance',
    ],
    'data': [
        'data/ir_cron.xml',
        'data/email_template.xml',
        'views/resource_calendar.xml',
        'views/hr_employee.xml'
    ],
    'installable': True,
}
