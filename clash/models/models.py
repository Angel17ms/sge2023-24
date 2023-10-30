# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Player(models.Model):
    _name = 'clash.player'
    _description = 'Player of Clash of War'

    name = fields.Char()
    level = fields.Integer(default=1)
    village_id = fields.Many2one('clash.village', string='Village')

class Village(models.Model):
    _name = 'clash.village'
    _description = 'Village in Clash of War'

    name = fields.Char()
    city_hall_level = fields.Integer(default=1)
    resources = fields.One2many('clash.resource', 'village_id')
    buildings = fields.One2many('clash.building', 'village_id')
    defenses = fields.One2many('clash.defense', 'village_id')

class Resource(models.Model):
    _name = 'clash.resource'
    _description = 'Resources in Clash of War'

    name = fields.Char()
    type = fields.Selection([('1', 'Gold'), ('2', 'Mana'), ('3', 'Gems')], string='Resource Type')
    village_id = fields.Many2one('clash.village', string='Village')

class BuildingType(models.Model):
    _name = 'clash.building_type'
    _description = 'Building Types in Clash of War'

    name = fields.Char()
    gold_production = fields.Float(string='Gold Production')
    mana_production = fields.Float(string='Mana Production')
    gems_production = fields.Float(string='Gems Production')
    health = fields.Float()

class Building(models.Model):
    _name = 'clash.building'
    _description = 'Buildings in Clash of War'

    name = fields.Char()
    type_id = fields.Many2one('clash.building_type', string='Building Type')
    village_id = fields.Many2one('clash.village', string='Village')
    troops = fields.One2many('clash.troop_type', 'camp_id')
    troops_max = fields.Integer(string='Maximum Troops Capacity')
    level = fields.Integer()

class DefenseType(models.Model):
    _name = 'clash.defense_type'
    _description = 'Defense Types in Clash of War'

    name = fields.Char()
    damage = fields.Float()
    health = fields.Float()

class Defense(models.Model):
    _name = 'clash.defense'
    _description = 'Defenses in Clash of War'

    name = fields.Char()
    type_id = fields.Many2one('clash.defense_type', string='Defense Type')
    village_id = fields.Many2one('clash.village', string='Village')
    level = fields.Integer()

class TroopType(models.Model):
    _name = 'clash.troop_type'
    _description = 'Troop Types in Clash of War'

    name = fields.Char()
    damage = fields.Float()
    health = fields.Float()
    cost_of_production = fields.Float(string='Production Cost')
    number_of_troops = fields.Integer(string='Number of Troops')
    camp_id = fields.Many2one('clash.building', string='Camp')

    def check_troop_limit(self):
        for troop_type in self:
            max_troops = troop_type.camp_id.troops_max
            total_troops = troop_type.camp_id.troops.number_of_troops + troop_type.number_of_troops
            raise ValidationError('Total number of troops exceeds the camp limit. Maximum allowed: %s' % total_troops)
            if total_troops > max_troops:
                raise ValidationError('Total number of troops exceeds the camp limit. Maximum allowed: %s' % max_troops)
