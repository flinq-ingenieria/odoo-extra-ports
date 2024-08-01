# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, api
from datetime import datetime
from datetime import timedelta
from pytz import timezone

class HrAttendance(models.Model):

    _inherit = 'hr.attendance'

    def get_nearest_interval(self, intervals, employee):
        empleado_tz = timezone(employee.tz)
        closest_time = False
        closest_interval = False
        for interval in intervals:
            if interval[1] > datetime.now(empleado_tz):
                return False
            if not closest_time or (datetime.now(empleado_tz) - interval[1]).seconds \
                    < closest_time:
                closest_time = (datetime.now(empleado_tz) - interval[1]).seconds < \
                    closest_time
                closest_interval = interval
        if not closest_interval:
            raise Exception(
                'Interval not found for employee %s' % employee.name)
        return closest_interval

    @api.model
    def cron_attendance_reminder(self):
        for employee in self.env['hr.employee'].search(
                [('resource_calendar_id', '!=', False)]):
            currently_working = employee.attendance_state == 'checked_in' and True or False
            calendar = employee.resource_calendar_id

            empleado_tz = timezone(employee.tz)
            today = datetime.now(empleado_tz).date()
            start_dt = empleado_tz.localize(datetime.combine(today, datetime.min.time()))
            end_dt = empleado_tz.localize(datetime.combine(today, datetime.max.time()))
            intervals = calendar._attendance_intervals_batch(start_dt, end_dt, resources=employee.resource_id)

            if intervals:
               intervals = intervals[0]
            if currently_working:
                if intervals:
                    nearest_interval = self.get_nearest_interval(
                        intervals, employee)
                    if not nearest_interval:
                        continue
                    if (datetime.now(empleado_tz) - nearest_interval[1]).seconds \
                            / 60.0 / 60.0 > 1:
                        # Aunque ya se haya pasado el momento de salida,
                        # si ya ha pasado mas de 1 hora no se envia,
                        # para evitar el envio continuo de emails.
                        continue
                template_id = self.env.ref('hr_attendance_reminder.email_template_attendance_reminder')
                template_id.send_mail(employee.id, force_send=True)
            else:
                for interval in intervals:
                    if interval[1] < datetime.now(empleado_tz) or \
                                interval[0] > datetime.now(empleado_tz):
                        continue
                    if interval[0] < datetime.now(empleado_tz) + \
                            timedelta(minutes=-calendar.reminder_delay) and \
                            (datetime.now(empleado_tz) - interval[0]).seconds\
                            / 60.0 / 60.0 < 1:
                        template_id = self.env.ref('hr_attendance_reminder.email_template_attendance_reminder')
                        template_id.send_mail(employee.id, force_send=True)
                        break
