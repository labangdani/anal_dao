# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Caracteristique(models.Model):
    _name = 'caracteristique.equipement'
    _description = 'caracteristique equipement'

    name = fields.Text(string="caractéristique")

class Notation(models.Model):
    _name = 'notation.equip'
    _description = 'notation'

    name = fields.Many2one('caracteristique.equipement', string = 'caractéristique')
    note = fields.Integer()
    ponderation = fields.Integer()
    observation = fields.Text()

class Equipement(models.Model):
    _name = 'equipement'
    _description = 'équipements'

    name = fields.Text(string="équipement")


class DetailEquipement(models.Model):

    _name = 'detail.equipement'
    _description = 'detail equipement'

    name = fields.Many2one("equipement", string="Equipement", required=True)
    unite = fields.Selection([
        ('u', "Unité"),
        ('ff', "Forfait"),
        ('h/j',"H/J"),
        ('h/m', "H/M")], string="Unité", required=True)
    quantite = fields.Integer(string="Quantité", required=True)
    prixu = fields.Float(string="Prix Unitaire", required=True)
    devise_id = fields.Many2one("devise", string="monnaie", required=True)
    prix_total = fields.Float(string="prix total", store=True, compute="compute_prix_total")
    total_fcfa = fields.Float(string="Prix total en FCFA", store=True ,compute="compute_total_fcfa") 
    modele = fields.Char(string="Modèle proposé")
    reference = fields.Char(string="Référence") 
    lien_equipement = fields.Char(string="Lien équipement")  
    lien_prix = fields.Char(string="Lien prix")  
    fournisseur = fields.Many2one('res.partner', string='Fournisseur')
    local = fields.Boolean(required=True)
    type_ressource = fields.Selection([
        ('humaine', "Humaine"),
        ('logiciel', "Logiciel"),
        ('materiel',"Matériel"),
        ('service', "Service")], string='Type ressource', required=True)

    caracteristique_ids = fields.Many2many('notation.equip', string="Caractéristique")
    sous_total_equip = fields.Integer(string="caractéristiques techniques",store=True, compute='compute_sous_total_equip')

    # projet_id = fields.Many2one("anal.projet") 
    pufcfa = fields.Float(compute="compute_pufcfa", store=True, string="prix unitaire en fcfa")
    transportu = fields.Float(compute="compute_transport_u", store=True,  string="transport par unité")
    transport_total= fields.Float(compute="compute_tranport_total", store=True, string="transport total")
    cout_achat = fields.Float(compute="compute_cout_achat", store=True, string="coût d'achat")
    douane_unite = fields.Float(compute="compute_douane_unite", store=True, string="Douane par unité")
    douane_total = fields.Float(compute="compute_douane_total", store=True, string="Douane total")
    cout_ru = fields.Float(compute="compute_cout_ru", store=True, string="Coût de revient par unité")
    cout_rt = fields.Float(compute="compute_cout_rt", store=True, string="Coût de revient total")
    marge_brute_u = fields.Float(compute="compute_marge_brute_u", store=True, string="Marge brute par unité")
    marge_brute_t = fields.Float(compute="compute_marge_brute_t", store=True, string="Marge brute total")
    prix_vente_u = fields.Float(compute="compute_prix_vente_u", store=True, string="Prix de vente par unité") 
    prix_vente_t = fields.Float(compute="compute_prix_vente_t", store=True, string="Prix de vente total")


    @api.depends('caracteristique_ids')
    def  compute_sous_total_equip(self):
        for equipement in self:
            sous_total_equip = 0
            for line in equipement.caracteristique_ids: 
                sous_total_equip += line.note
            equipement.update({
                'sous_total_equip': sous_total_equip,
            })


    @api.constrains()
    def set_to_humaine(self):
        return self.write({'type_ressource' : 'humaine'})
    
    def set_to_logiciel(self):
        return self.write({'type_ressource' : 'logiciel'})

    def set_to_materiel(self):
        return self.write({'type_ressource' : 'materiel'})

    def set_to_service(self):
        return self.write({'type_ressource' : 'service'})

    @api.depends('prixu', 'quantite')
    def  compute_prix_total(self):
        self.prix_total = self.prixu * self.quantite


    @api.depends('prix_total', 'devise_id')
    def  compute_total_fcfa(self):
        self.total_fcfa = self.prix_total * self.devise_id.taux

    @api.depends('total_fcfa', 'quantite')
    def  compute_pufcfa(self):
        if self.quantite != 0:
            self.pufcfa = self.total_fcfa/self.quantite
        else:
            self.pufcfa = 0

    @api.depends('local', 'type_ressource', 'pufcfa')
    def compute_transport_u(self):
        params = self.env['parametre'].search([])
        taux =params[2].value1
        if self.local == False and (self.type_ressource != "logiciel" and self.type_ressource != "service"):
            self.transportu = (self.pufcfa*taux)/100
        else:
            self.transportu = 0  

    @api.depends('transportu', 'quantite')
    def compute_tranport_total(self):
        self.transport_total = self.transportu * self.quantite

    @api.depends('pufcfa', 'transportu')
    def compute_cout_achat(self):
        self.cout_achat = self.pufcfa + self.transportu

    @api.depends('local', 'type_ressource', 'cout_achat')
    def compute_douane_unite(self):
        params = self.env['parametre'].search([])
        taux_douane = params[0].value1
        if self.local == False and (self.type_ressource != "logiciel" and self.type_ressource != "service"):
            self.douane_unite = (self.cout_achat*taux_douane)/100
        else:
            self.douane_unite = 0     

    @api.depends('douane_unite', 'quantite')
    def compute_douane_total(self):
        self.douane_total = self.douane_unite * self.quantite

    @api.depends('cout_achat', 'douane_unite')
    def compute_cout_ru(self):
        self.cout_ru = self.cout_achat + self.douane_unite

    @api.depends('cout_ru', 'quantite')
    def compute_cout_rt(self):
        self.cout_rt = self.cout_ru * self.quantite   

    @api.depends('cout_ru')
    def compute_marge_brute_u(self):
        params = self.env['parametre'].search([])
        taux_marge_brut =params[1].value1
        self.marge_brute_u = (self.cout_ru * taux_marge_brut)/100

    @api.depends('marge_brute_u', 'quantite')
    def compute_marge_brute_t(self):
        self.marge_brute_t = self.marge_brute_u * self.quantite    

    @api.depends('marge_brute_u', 'cout_ru')
    def compute_prix_vente_u(self):
        self.prix_vente_u = self.marge_brute_u + self.cout_ru 

    @api.depends('prix_vente_u', 'quantite')
    def compute_prix_vente_t(self):
        self.prix_vente_t = self.prix_vente_u * self.quantite            

      



    

    
        
    
