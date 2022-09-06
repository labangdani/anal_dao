# -*- coding: utf-8 -*-

from odoo import models, fields, api
  
class Caracteristique(models.Model):
    _name = 'detail.critere'
    _description = 'détail des critères'

    name = fields.Text(string="designation")

class Critere(models.Model):
    _name = 'critere'
    _description = 'critères'

    name = fields.Char(string="Désignation", required=True)
    evaluation = fields.Selection([
        ('oui', 'OUI'),
        ('non', 'NON')], string='Evaluation', required=True, index=True)
    observation = fields.Text()
    is_essentiel = fields.Boolean()
    

    

class grillenotation(models.Model):
    _name = 'grille.critere'
    _description = 'grille critères essentiels'

    critere_ids = fields.Many2one('critere')
    # name = fiels.Char(related='critere_ids.name')
    sous_total_note = fields.Integer(store=True, compute='compute_total_notation')
    sous_total_ponderation = fields.Integer(store=True, compute='compute_total_notation')
    notation_ids = fields.Many2many('notation', string="Sous critères")
    projet_id = fields.Many2one('anal.projet')

    @api.depends('notation_ids')
    def  compute_total_notation(self):
        for critere in self:
            sous_total_ponderation = sous_total_note = 0
            for line in critere.notation_ids: 
                sous_total_note += line.note
                sous_total_ponderation += line.ponderation
            critere.update({
                'sous_total_note': sous_total_note,
                'sous_total_ponderation': sous_total_ponderation,
            })


# class criterenotation(models.Model):
#     _name = 'res.critere'
#     _description = 'critères notation'

#     name = fields.Text(string='nom', ondelete=False)


class Notation(models.Model):
    _name = 'notation'
    _description = 'notation'
    _rec_name = 'detail_critere_id'

    detail_critere_id = fields.Many2one('detail.critere', string = 'détail')
    note = fields.Integer()
    ponderation = fields.Integer()
    observation = fields.Text()

class CritereEvaluation(models.Model):

    _name = 'critere.evaluation'
    _description = 'critère d\'évaluation'
    _rec_name = 'categorie'

    categorie = fields.Selection([
        ('equipe','Equipe'),
        ('essentiel','Critères Essentiels'),
        ('eliminatoire','Critères Eliminatoires'),
        ('dossier','Dossier administratif'),
        ('specification','Spécification'),
        ('offre','Offre financière'),
        ('garantie','Garantie fourniture'),
        ('modalite','Modalité de reception')], required=True, string='Catégorie')
    total = fields.Text(string="Total", store=True, compute='compute_total') 
    critere_ids = fields.Many2many('critere', string="Critères")
    projet_id = fields.Many2one("anal.projet") 


    @api.depends('critere_ids')
    def  compute_total(self):
        nb_critere = len(self.critere_ids)
        print(nb_critere)
        nbr_total_oui = 0
        for elt in self.critere_ids:
            if elt.evaluation == 'oui':
                nbr_total_oui = nbr_total_oui + 1
        if nbr_total_oui >= (nb_critere*(3/5)):
            print(nbr_total_oui)        
            self.total = "OK"
        else:
            self.total = "NOT OK"



       

