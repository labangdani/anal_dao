# -*- coding: utf-8 -*-

from odoo import models, fields, api
  
class DevisEstimatif(models.Model):

    _name = 'compte.exploi'
    _description = "compte d'exploitation"

    name = fields.Text(required=True)
    projet_id = fields.Many2one("anal.projet")
    equipements = fields.Many2many(related='projet_id.detail_equipement_ids', readonly=True)
    devis = fields.Many2one(related='projet_id.devis_id', readonly=True)
    save_marche = fields.Integer(store=True, string="Enregistrement marché")
    frais_caution_def = fields.Integer(store=True, string="Frais caution définitive")
    frais_caution_gar = fields.Integer(store=True, string="Frais caution garantie")
    frais_approche = fields.Integer(store=True, string="Frais d'approche")
    jetons = fields.Integer(store=True, string="Jetons de présence réunion de reception provisoire ou définitive")
    imprevu = fields.Integer(store=True, string="Imprévus")
    total_autre_charge = fields.Integer(store=True, string="Total d'autres charges")
    achat_total = fields.Integer(store=True, string="Achat total")
    total_charge = fields.Integer(store=True, string="Total charges du projet")
    taux_marge = fields.Integer(store=True, string="Taux de marge sur projet")
    marge = fields.Integer(store=True, string="Marge du projet")

    # @api.depends('projet_id')
    # def compute_name(self):
    #     self.name = 'compte d\'exploitation du ' + self.projet_id.name

    # @api.depends('devis_id')
    # def compute_save_marche(self):
    #     if self.devis_id.total_general < 5000001:
    #         self.save_marche = self.devis_id.total_general*0.07
    #     else:
    #         if self.devis_id.total_general < 50000001:
    #             self.save_marche = self.devis_id.total_general*0.05
    #         else:
    #             self.save_marche = self.devis_id.total_general*0.03
    
    # @api.depends('devis_id')
    # def compute_frais_caution_def(self):
    #     self.frais_caution_def = self.devis_id.total_ttc*0.05*0.02

    # @api.depends('devis_id')
    # def compute_frais_caution_gar(self):
    #     self.frais_caution_gar = self.devis_id.total_ttc*0.1*0.02

    # @api.depends('devis_id')
    # def compute_frais_approche(self):
    #     params = self.env['parametre'].search([])
    #     taux_frais_approche =params[3].value1
    #     self.frais_approche = taux_frais_approche*self.devis_id.total_general

    # @api.depends('devis_id')
    # def compute_jetons(self):
    #     params = self.env['parametre'].search([])
    #     taux_jetons = params[4].value1
    #     self.jetons = taux_jetons*self.devis_id.total_general 

    # @api.depends('devis_id')
    # def compute_imprevu(self):
    #     params = self.env['parametre'].search([])
    #     taux_imprevu = params[5].value1
    #     self.imprevu = taux_imprevu*self.devis_id.total_general

    # @api.depends('achat_dao','caution_soumission','frais_timbre_s','frais_timbre_d','save_marche','frais_caution_def','frais_caution_gar','frais_approche','jetons','imprevu')
    # def compute_total_autre_charge(self):
        
    #     x = self.achat_dao + self.caution_soumission + self.frais_timbre_s + self.frais_timbre_d + self.save_marche + self.frais_caution_def + self.frais_caution_gar + self.frais_approche + self.jetons + self.imprevu
    #     print(type(x))              
    #     self.total_autre_charge = self.achat_dao + self.caution_soumission + self.frais_timbre_s + self.frais_timbre_d + self.save_marche + self.frais_caution_def + self.frais_caution_gar + self.frais_approche + self.jetons + self.imprevu               


    # @api.depends('devis_id')
    # def compute_achat_total(self):
    #     params = self.env['parametre'].search([])
    #     taux_douane = params[0].value1
    #     douane = ((self.devis_id.total_etranger+self.devis_id.total_transport)*taux_douane)/100
    #     self.achat_total = self.devis_id.total_transport+self.devis_id.total_etranger+self.devis_id.total_local+douane

    # @api.depends('total_autre_charge','achat_total')
    # def compute_total_charge(self):
    #     self.total_charge = self.total_autre_charge + self.achat_total 

    # @api.depends('devis_id','total_charge')
    # def compute_taux_marge(self):
    #     if self.devis_id.total_general != 0: 
    #         x = (self.devis_id.total_general - self.total_charge )/self.devis_id.total_general
    #         # self.write({'taux_marge':round(x,2)}) 
    #         self.taux_marge = x
    #     else:
    #         self.taux_marge = 0     