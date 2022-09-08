# -*- coding: utf-8 -*-
import base64
import hashlib



from odoo import models, fields, api

class Marche_type_dao(models.Model):

    _name = 'type.dao'
    _description = 'Type appel d\'offre'

    code = fields.Char('Code', required=True)
    name = fields.Char('Libellé', required=True)   

class Marche(models.Model):
    _name = 'anal.projet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'anal projet'


    name = fields.Text(string="Intitulé du projet", required=True)
    type_dao_id = fields.Many2one(string='Type DAO',comodel_name='type.dao',ondelete='restrict', required=True)
    moa = fields.Many2one('res.partner', string='Maitre d\'ouvrage', required=True, 
        domain=[('is_ressource','=',False),('is_entity','=', False)])
    objet = fields.Text(string="L'objet de l'appel d'offre")
    date_depot = fields.Datetime(string="Date limite de dépôt", default=fields.Datetime.now)
    delai_execution = fields.Integer(string="Délai d'exécution (en jours)")
    financement = fields.Char(string="Financement")
    date_debut = fields.Date(string="Date début des travaux", default=fields.Datetime.now)
    state = fields.Selection([
        ('0draft', "Nouveau"),
        ('1analyse', "En cours d'analyse"),
        ('2evaluate', "En cours d'évaluation"),
        ('3submit',"En cours de soumission"),
        ('4submited', "Dossier soumissionné"),
        ('5qualified', "Qualifié"),
        ('6cancel', "Annulé"),
        ('7reported', "Reporté"),
        ('8win', "Gagné"),
        ('9lost', "Perdu"),
        ('10aborted', "Abandonné"),], string='Statut', required=True, default='0draft')
    color = fields.Integer('Color Index', default=0)
    date_submit = fields.Date(string="date de soumission")
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Very High')], string='Priorité', index=True, default='0')    
    
    note = fields.Text() 
    totaux_technique = fields.Integer(string="Caractéristiques techniques total", store=True, readonly=True, compute='compute_totaux_technique')
    totaux_critere = fields.Integer(string="Critères essentiels", store=True, readonly=True, compute='_amount_all')
    total_ponderation = fields.Integer(store=True, readonly=True, compute='_amount_all')       
    budget = fields.Integer(string="Budget de l'offre", currency_field='company_currency', tracking=True)

    detail_equipement_ids = fields.Many2many('detail.equipement', string='detail équipement', required=True)
    total_etranger = fields.Integer(string='Total étranger', compute='compute_total_etranger')
    achat_dao = fields.Integer(string="Achat DAO")
    caution_soumission = fields.Integer(string="Caution de soumission")
    frais_timbre_s = fields.Integer(string="Frais de timbres pour soumission")
    frais_timbre_d = fields.Integer(string="Frais timbres pour dossier paiement")

    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    company_currency = fields.Many2one("res.currency", string='Currency', related='company_id.currency_id', readonly=True)
    
    critere_evaluation_ids = fields.One2many('critere.evaluation', 'projet_id', string='critère d\'évaluation') 
    grille_notation_ids = fields.One2many('grille.critere', 'projet_id', string='grille de notation')
    compte_exist = fields.Boolean()
    devis_exist = fields.Boolean()
    devis_id = fields.Many2one("devis.estimatif")
    compte_exploi_id = fields.Many2one("compte.exploi")
 




 
    # @api.constrains('date_depot','date_debut') 
    # def _check_date_debut(self):
    #     if self.date_depot > self.date_debut:
    #         raise ValidationError('Erreur! La date de depot du projet doit être inferieur à la date de debut du projet') 

    # @api.constrains('date_depot','date_submit')
    # def _check_date_submit(self):
    #     if self.date_depot > self.date_submit:
    #         raise ValidationError('Erreur! La date de depot du projet doit être inferieur à la date de soumission du projet')               

 
    @api.depends('grille_notation_ids')
    def _amount_all(self):
        for projet in self:
            total_ponderation = totaux_critere = 0
            for line in projet.grille_notation_ids:
                totaux_critere += line.sous_total_note
                total_ponderation += line.sous_total_ponderation
            projet.update({
                'totaux_critere': totaux_critere,
                'total_ponderation': total_ponderation,
            })

    @api.depends('detail_equipement_ids')
    def compute_totaux_technique(self):
        for projet in self:
            totaux_technique = 0
            for line in projet.detail_equipement_ids:
                print(line)
                totaux_technique += line.sous_total_equip
            projet.update({
                'totaux_technique': totaux_technique,
            })        


    @api.depends('detail_equipement_ids')
    def compute_total_etranger(self):
        for elt in self.detail_equipement_ids:
            if elt.local == False:
                self.total_etranger = self.total_etranger + elt.prix_vente_t        


    @api.constrains()
    def set_to_draft(self):
        return self.write({'state' : '0draft'})

    def set_to_analyse(self):
        
        return self.write({'state' : '1analyse'})

    def set_to_evaluate(self):
        return self.write({'state' : '2evaluate'}) 

    def set_to_submit(self):
        return self.write({'state' : '3submit'})
    
    def set_to_qualified(self):
        return self.write({'state' : '5qualified'})

    def set_to_cancel(self):
        return self.write({'state' : '6cancel'})

    def set_to_reported(self):
        return self.write({'state' : '7reported'})

    def set_to_win(self):
        return self.write({'state' : '8win'})    

    def set_to_lost(self, **additional_values):
        """ Lost semantic: probability = 0 or active = False """
        res = self.action_archive()
        if additional_values:
            self.write(dict(additional_values))
        return res

    def set_to_aborted(self):
        return self.write({'state' : '10aborted'})    

############### generate devis estimatif   ###################
    
    def createdevis(self):
        params = self.env['parametre'].search([])
        tva =params[6].value1
        air =params[7].value1
        total_etranger = total_local = total_general = total_transport = total_tva = total_air = total_ttc = net_gagner = 0
        for line in self.detail_equipement_ids:
            if line.local == False:
                total_etranger += line.prix_vente_t
            else:
                total_local += line.prix_vente_t
            total_transport += line.transport_total    
            total_general += line.prix_vente_t 
        total_tva = (total_general*tva)/100
        total_air = (total_general*air)/100
        total_ttc = total_general + total_tva
        net_gagner = total_general - total_air      
        self.devis_id = self.env['devis.estimatif'].create({
            'projet_id':self.id,
            'name': 'devis du ' + self.name,
            'total_etranger':total_etranger,
            'total_local':total_local,
            'total_general':total_general,
            'total_transport':total_transport,
            'total_tva':total_tva,
            'total_air':total_air,
            'total_ttc':total_ttc,
            'net_gagner':net_gagner,
        })
        self.write({'devis_exist': True})


    def updatedevis(self):
        devis_estimatif = self.env['devis.estimatif'].search([('projet_id','=',self.id)])
        params = self.env['parametre'].search([])
        tva =params[6].value1
        air =params[7].value1
        total_etranger = total_local = total_general = total_transport = total_tva = total_air = total_ttc = net_gagner = 0
        for line in self.detail_equipement_ids:
            if line.local == False:
                total_etranger += line.total_fcfa
            else:
                total_local += line.total_fcfa
            total_transport += line.transport_total    
        total_general = total_etranger + total_local 
        total_tva = (total_general*tva)/100
        total_air = (total_general*air)/100
        total_ttc = total_general + total_tva
        net_gagner = total_general - total_air      
        devis_estimatif.update({
            'total_etranger':total_etranger,
            'total_local':total_local,
            'total_general':total_general,
            'total_transport':total_transport,
            'total_tva':total_tva,
            'total_air':total_air,
            'total_ttc':total_ttc,
            'net_gagner':net_gagner,
        })


############### generate compte d'exploitation   ###################

    def createcompte(self):
        params = self.env['parametre'].search([])
        taux_frais_approche =params[3].value1
        taux_jetons = params[4].value1
        taux_imprevu = params[5].value1
        taux_douane = params[0].value1
        if self.devis_id:
            if self.devis_id.total_general < 5000001:
                save_marche = self.devis_id.total_general*0.07
            else:
                if self.devis_id.total_general < 50000001:
                    save_marche = self.devis_id.total_general*0.05
                else:
                    save_marche = self.devis_id.total_general*0.03
            frais_caution_def = self.devis_id.total_ttc*0.05*0.02
            frais_caution_gar = self.devis_id.total_ttc*0.1*0.02
            frais_approche = taux_frais_approche*self.devis_id.total_general
            jetons = taux_jetons*self.devis_id.total_general
            imprevu = taux_imprevu*self.devis_id.total_general
            total_autre_charge = self.achat_dao + self.caution_soumission + self.frais_timbre_s + self.frais_timbre_d + save_marche + frais_caution_def + frais_caution_gar + frais_approche + jetons + imprevu                
            douane = ((self.devis_id.total_etranger+self.devis_id.total_transport)*taux_douane)/100
            achat_total = self.devis_id.total_transport+self.devis_id.total_etranger+self.devis_id.total_local+douane
            total_charge = total_autre_charge + achat_total 
            if self.devis_id.total_general != 0: 
                x = (self.devis_id.total_general - total_charge )/self.devis_id.total_general
                taux_marge = x
            else:
                taux_marge = 0 
            marge = self.devis_id.total_general - total_charge
            print(self.devis_id)      
            self.compte_exploi_id = self.env['compte.exploi'].create({
                    'projet_id':self.id,
                    'name': 'compte d\'exploitation du ' + self.name,
                    'save_marche':save_marche,
                    'frais_caution_def':frais_caution_def,
                    'frais_caution_gar':frais_caution_gar,
                    'frais_approche':frais_approche,
                    'jetons':jetons,
                    'imprevu':imprevu,
                    'total_autre_charge':total_autre_charge,
                    'achat_total':achat_total,
                    'total_charge':total_charge,
                    'taux_marge':taux_marge,
                    'marge':marge,
    
                })
        self.compte_exist = True    


    def updatecompte(self):
        compte_exploi = self.env['compte.exploi'].search([('projet_id','=',self.id)])
        params = self.env['parametre'].search([])
        taux_frais_approche =params[3].value1
        taux_jetons = params[4].value1
        taux_imprevu = params[5].value1
        taux_douane = params[0].value1
        if self.devis_id:
            if self.devis_id.total_general < 5000001:
                save_marche = self.devis_id.total_general*0.07
            else:
                if self.devis_id.total_general < 50000001:
                    save_marche = self.devis_id.total_general*0.05
                else:
                    save_marche = self.devis_id.total_general*0.03
            frais_caution_def = self.devis_id.total_ttc*0.05*0.02
            frais_caution_gar = self.devis_id.total_ttc*0.1*0.02
            frais_approche = taux_frais_approche*self.devis_id.total_general
            jetons = taux_jetons*self.devis_id.total_general
            imprevu = taux_imprevu*self.devis_id.total_general
            total_autre_charge = self.achat_dao + self.caution_soumission + self.frais_timbre_s + self.frais_timbre_d + save_marche + frais_caution_def + frais_caution_gar + frais_approche + jetons + imprevu                
            douane = ((self.devis_id.total_etranger+self.devis_id.total_transport)*taux_douane)/100
            achat_total = self.devis_id.total_transport+self.devis_id.total_etranger+self.devis_id.total_local+douane
            total_charge = total_autre_charge + achat_total 
            if self.devis_id.total_general != 0: 
                x = (self.devis_id.total_general - total_charge )/self.devis_id.total_general
                taux_marge = x
            else:
                taux_marge = 0 
            marge = self.devis_id.total_general - total_charge           
            compte_exploi.update({
                    'save_marche':save_marche,
                    'frais_caution_def':frais_caution_def,
                    'frais_caution_gar':frais_caution_gar,
                    'frais_approche':frais_approche,
                    'jetons':jetons,
                    'imprevu':imprevu,
                    'total_autre_charge':total_autre_charge,
                    'achat_total':achat_total,
                    'total_charge':total_charge,
                    'taux_marge':taux_marge,
                    'marge':marge,
    
                })         
    


class icc_anal_base(models.Model):
    _name = 'parametre'
    _description = 'parametre'

    name = fields.Text()
    value1 = fields.Float()
    value2 = fields.Float()
    value3 = fields.Float()


class cle_repartition(models.Model):
    _name = 'cle.repartition'
    _description = 'cle repartition'

    cout_achat = fields.Float(string="coût d'achat")
    transport = fields.Float(string="transport")
    cout_commande = fields.Float(string="coût commande")
    frais_livraison = fields.Float(string= "frais de livraison")
    marge = fields.Float(string="marge")
    materiel = fields.Boolean(string="matériel")
    logiciel = fields.Boolean(string="logiciel")

class devise(models.Model):
    _name = 'devise'
    _description = 'devise'

    name = fields.Text()
    taux = fields.Float()


   
