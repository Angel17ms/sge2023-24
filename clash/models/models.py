# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Player(models.Model):
    _name = 'clash.player'
    _description = 'Player of Clash of War'

    name = fields.Char()
    level = fields.Integer(default = 1)


class Village(models.Model):
    _name = 'clash.village'
    _description = 'Village of Clash of War'

    name = fields.Char()
    city_hall_level = fields.Integer(default = 1)
    resoureces = fields.One2many('clash.Resources', 'aldea')
    build = fields.One2many('clash.build', 'city')
    defenses = fields.One2many('clash.Defenses', 'city')

    

class Resources(models.Model):
    _name = 'clash.Resources'
    _description = 'Resources of Clash of War'

    name = fields.Char()
    type = fields.Selection([('1', 'Gold'), ('2', 'Mana'), ('3', 'Gems'), ('4', 'Trops')])
    aldea = fields.Many2one('clash.village')



class Building_Types(models.Model):
    _name = 'clash.Buildings'
    _description = 'Types of build in Clash of War'

    name = fields.Char()
    gold_production = fields.Float()
    mana_production = fields.Float()
    gems_production = fields.Float()
    trops_production = fields.Float()
    builds = fields.One2many('clash.build', 'type')


class Build(models.Model):
    _name = 'clash.build'
    _description = 'Builds of Clash of War'

    name = fields.Char()
    type = fields.Many2one('clash.Buildings')
    city = fields.Many2one('clash.village')
    level = fields.Integer()


class Defenses(models.Model):
    _name = 'clash.Defenses'
    _description = 'Types of build in Clash of War'

    name = fields.Char()
    cannons = fields.Integer()
    mortar = fields.Integer()
    archer_tower = fields.Integer()
    infernal_tower = fields.Integer()
    crossbow = fields.Integer()
    city = fields.Many2one('clash.village')
