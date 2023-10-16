# -*- coding: utf-8 -*-

from odoo import models, fields, api


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
    type = fields.Selection([('1', 'Gold'), ('2', 'Mana'), ('3', 'Gems'), ('4', 'Trops')])
    aldea = fields.Many2one('clash.village')



class building_types(models.Model):
    _name = 'clash.building_types'
    _description = 'Types of build in Clash of War'

    name = fields.Char()
    gold_production = fields.Float()
    mana_production = fields.Float()
    gems_production = fields.Float()
    trops_production = fields.Float()


class build(models.Model):
    _name = 'clash.build'
    _description = 'Builds of Clash of War'

    name = fields.Char()
    type = fields.Many2one('clash.building_types')
    city = fields.Many2one('clash.village')
    level = fields.Integer()


class defenses(models.Model):
    _name = 'clash.defenses'
    _description = 'Types of build in Clash of War'

    name = fields.Char()
    cannons = fields.Integer()
    mortar = fields.Integer()
    archer_tower = fields.Integer()
    infernal_tower = fields.Integer()
    crossbow = fields.Integer()
    city = fields.Many2one('clash.village')
