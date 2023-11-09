# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Player(models.Model):
    _name = 'clash.player'
    _description = 'Player of Clash of War'

    name = fields.Char()
    level = fields.Integer(default=1)
    village_id = fields.Many2one('clash.village', string='Village')

    @api.constrains('level')
    def check_level(self):
        for player in self:
            if player.level < 1:
                raise ValidationError('The level of player cannot be lower to 1')

class Village(models.Model):
    _name = 'clash.village'
    _description = 'Village in Clash of War'

    name = fields.Char()
    city_hall_level = fields.Integer(default=1)
    resources = fields.One2many('clash.resource', 'village_id')
    buildings = fields.One2many('clash.building', 'village_id')
    defenses = fields.One2many('clash.defense', 'village_id')

    @api.constrains('city_hall_level')
    def check_level(self):
        for village in self:
            if village.city_hall_level < 1:
                raise ValidationError('The level of city hall cannot be lower to 1')

class Resource(models.Model):
    _name = 'clash.resource'
    _description = 'Resources in Clash of War'

    name = fields.Char()
    type = fields.Selection([('1', 'Gold'), ('2', 'Mana'), ('3', 'Gems')], string='Resource Type')
    village_id = fields.Many2one('clash.village', string='Village')

class Building(models.Model):
    _name = 'clash.building'
    _description = 'Buildings in Clash of War'

    name = fields.Char()
    type = fields.Selection([('1','Mina'),('2','Recolector'),('3','Extractor'),('4','Campamento')], default = '1')
    gold_production = fields.Float(string='Gold Production', compute = 'set_resources')
    mana_production = fields.Float(string='Mana Production', compute = 'set_resources')
    gems_production = fields.Float(string='Gems Production', compute = 'set_resources')
    health = fields.Float()
    village_id = fields.Many2one('clash.village', string='Village')
    troops = fields.One2many('clash.troop_type', 'camp_id')
    current_troops =fields.Integer(compute='check_current_troops')
    troops_max = fields.Integer(string='Maximum Troops Capacity', compute = 'set_resources')
    level = fields.Integer(default=1)

    @api.depends('type')
    def set_resources(self):
        print()
        for b in self:
            
            b.gold_production = 0
            b.mana_production = 0.0
            b.gems_production = 0.0
            b.troops_max = 0
            if b.type == '1':
                b.gold_production = 100.0
                b.mana_production = 0.0
                b.gems_production = 0.0
                b.troops_max = 0
            if b.type == '2':
                b.gold_production = 0.0
                b.mana_production = 100.0
                b.gems_production = 0.0
                b.troops_max = 0
            if b.type == '3':
                b.gold_production = 0.0
                b.mana_production = 0.0
                b.gems_production = 20.0
                b.troops_max = 0
            if b.type == '4':
                b.gold_production = 0.0
                b.mana_production = 0.0
                b.gems_production = 0.0
                b.troops_max = 100

    @api.constrains('level')
    def check_level(self):
        for building in self:
            if building.level < 1:
                raise ValidationError('The level of building cannot be lower to 1')
    
    @api.depends('troops')
    def check_current_troops(self):
        for building in self:
            total_troops = sum(troop.number_of_troops for troop in building.troops)
            building.current_troops = total_troops

    


class Defense(models.Model):
    _name = 'clash.defense'
    _description = 'Defenses in Clash of War'

    name = fields.Char()
    type = fields.Selection([('1','Cañon'),('2','Torre de Francotirador'),('3','Mortero'), ('4','Ballesta')])
    damage = fields.Float()
    health = fields.Float()
    village_id = fields.Many2one('clash.village', string='Village')
    level = fields.Integer()

    @api.constrains('level')
    def check_level(self):
        for defense in self:
            if defense.level < 1:
                raise ValidationError('The level of defense cannot be lower to 1')

class TroopType(models.Model):
    _name = 'clash.troop_type'
    _description = 'Troop Types in Clash of War'

    name = fields.Char()
    damage = fields.Float()
    health = fields.Float()
    cost_of_production = fields.Float(string='Production Cost')
    number_of_troops = fields.Integer(string='Number of Troops')
    camp_id = fields.Many2one('clash.building', string='Camp')

    @api.constrains('number_of_troops')
    def check_troop_limit(self):
        for troop_type in self:
            if troop_type.number_of_troops < 1:
                raise ValidationError('The number of troops cannot be negative')

    @api.constrains('number_of_troops')
    def check_max_troops(self):
        for troops in self:
        
            if (troops.camp_id.current_troops > troops.camp_id.troops_max):
                raise ValidationError('You cannot exceed the maximum limit of a camp')
