# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class player(models.Model):
    _name = 'clash.player'
    _description = 'Player of Clash of War'

    name = fields.Char()
    level = fields.Integer(default = 1)


class village(models.Model):
    _name = 'clash.village'
    _description = 'Village of Clash of War'

    name = fields.Char()
    city_hall_level = fields.Integer(default = 1)
    resoureces = fields.One2many('clash.resource', 'aldea')
    build = fields.One2many('clash.build', 'city')
    defenses = fields.One2many('clash.defenses', 'city')

    

class resource(models.Model):
    _name = 'clash.resource'
    _description = 'Resources of Clash of War'

    name = fields.Char()
    type = fields.Selection([('1', 'Gold'), ('2', 'Mana'), ('3', 'Gems')])
    aldea = fields.Many2one('clash.village')



class building_types(models.Model):
    _name = 'clash.building_types'
    _description = 'Types of build in Clash of War'

    name = fields.Char()
    gold_production = fields.Float()
    mana_production = fields.Float()
    gems_production = fields.Float()
    trops_max = fields.Integer()
    health = fields.Float()


class build(models.Model):
    _name = 'clash.build'
    _description = 'Builds of Clash of War'

    name = fields.Char()
    type = fields.Many2one('clash.building_types')
    city = fields.Many2one('clash.village')
    trops = fields.One2many('clash.trops_type','campament')
    level = fields.Integer()


class defenses_type(models.Model):
    _name = 'clash.defenses_type'
    _description = 'Types of defenses in Clash of War'

    name = fields.Char()
    damage = fields.Float()
    health = fields.Float()


class defenses(models.Model):
    _name = 'clash.defenses'
    _description = 'Defenses in Clash of War'

    name = fields.Char()
    type = fields.Many2one('clash.defenses_type')
    city = fields.Many2one('clash.village')
    level = fields.Integer()


class trops_type(models.Model):
    _name = 'clash.trops_type'
    _description = 'Types of trops in Clash of War'

    name = fields.Char()
    damage = fields.Float()
    health = fields.Float()
    cost_of_production = fields.Float()
    number_of_troops = fields.Integer()
    campament = fields.Many2one('clash.build')

    @api.constrains('number_of_troops', 'campament')
    def check_troop_limit(self):
        for troop_type in self:
            max_troops = troop_type.campament.type.trops_max
            total_troops = sum(t.number_of_troops for t in troop_type.campament.trops)
            if total_troops + troop_type.number_of_troops > max_troops:
                raise ValidationError('Total number of troops exceeds the camp limit.')

