# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DevisEstimatif(models.Model):

    _name = 'devis.estimatif'
    _description = 'devis estimatif'

    name = fields.Text(required=True)
    projet_id = fields.Many2one("anal.projet", readonly=True) 
    equipements = fields.Many2many(related='projet_id.detail_equipement_ids', required=True, readonly=True)
    total_transport = fields.Integer(string="Transport total",store=True, readonly=True)
    total_etranger = fields.Integer(string="Sous total 1 : achat etranger", store=True, readonly=True)
    total_local = fields.Integer(string="Sous total 2 : achat local", store=True, readonly=True)
    total_general = fields.Integer(string="Total général", store=True, readonly=True)
    total_tva = fields.Integer(string="Total TVA", store=True, readonly=True)
    total_air = fields.Integer(string="Total AIR", store=True, readonly=True)
    total_ttc = fields.Integer(string="Total TTC", store=True, readonly=True)
    net_gagner = fields.Integer(string="Net à percevoir", store=True, readonly=True)

      

         