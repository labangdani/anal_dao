# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Submit(models.Model):
    _name = 'submit.dossier'
    _description = 'submit dossier '

    date = fields.Datetime(string="Date")

    def action_submit_projet(self):
        opportunity = self.env['anal.projet'].browse(self.env.context.get('active_ids'))
        opportunity.write({"date_submit":self.date,
                          "state":"submited"})


