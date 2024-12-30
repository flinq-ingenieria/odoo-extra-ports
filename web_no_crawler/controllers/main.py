# Copyright (C) 2018 Ventor, Xpansa Group (<https://ventor.tech/>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.http import Controller, request, route


class Main(Controller):

    @route('/robots.txt', type='http', auth="public")
    def robots(self):
        return request.make_response(
            "User-agent: *\nDisallow: /",
            headers=[('Content-Type', 'text/plain')],
        )
