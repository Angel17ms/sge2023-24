# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Player(models.Model):
    _name = 'clash.player'
    _description = 'Player of Clash of War'

    name = fields.Char()
    level = fields.Integer(default=1)
    village_id = fields.Many2one('clash.village', string='Village')
    village_level = fields.Integer(string='Nivel de aldea', related='village_id.city_hall_level', readonly=True)

    @api.constrains('level')
    def check_level(self):
        for player in self:
            if player.level < 1:
                raise ValidationError('The level of player cannot be lower than 1')

    @api.model
    def reset_properties(self):
        for player in self:
            if player.village_id:
                player.village_id.unlink()

            player.write({
                'level': 1,
                'village_id': None,
            })
        return True

    def action_reset_player_properties(self):
        players = self.env['clash.player'].search([])
        players.reset_properties()
        return True

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

    @api.model
    def update_resources(self):
        villages = self.search([])
        for village in villages:
            total_gold_production = 0
            total_mana_production = 0
            total_gems_production = 0

            for building in village.buildings:
                total_gold_production += building.gold_production
                total_mana_production += building.mana_production
                total_gems_production += building.gems_production

            resources = village.resources.filtered(lambda r: r.type in ('1', '2', '3'))
            for resource in resources:
                if resource.type == '1':
                    resource.amount += total_gold_production
                elif resource.type == '2':
                    resource.amount += total_mana_production
                elif resource.type == '3':
                    resource.amount += total_gems_production

            print("Update complete!")

        return True

    def button_increment_level(self):
        for village in self:
            village.write({'city_hall_level': village.city_hall_level + 1})
        return True

class Resource(models.Model):
    _name = 'clash.resource'
    _description = 'Resources in Clash of War'

    name = fields.Char()
    type = fields.Selection([('1', 'Gold'), ('2', 'Mana'), ('3', 'Gems')], string='Resource Type')
    amount = fields.Integer()
    village_id = fields.Many2one('clash.village', string='Village')

    @api.constrains('amount')
    def check_level(self):
        for resource in self:
            if resource.amount < 0:
                raise ValidationError('The amount cannot be negative')

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
    total_production_cost = fields.Float(string='Total Troop Production Cost', compute='calculate_total_production_cost')
    level = fields.Integer(default=1)
    

    @api.depends('type')
    def set_resources(self):
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

    @api.depends('troops')
    def calculate_total_production_cost(self):
        for building in self:
            total_cost = sum(troop.cost_of_production * troop.number_of_troops for troop in building.troops)
            building.total_production_cost = total_cost
    
    def button_increment_level(self):
        for builds in self:
            builds.write({'level': builds.level + 1})
        return True

class Defense(models.Model):
    _name = 'clash.defense'
    _description = 'Defenses in Clash of War'

    name = fields.Char()
    type = fields.Selection([('1','Cañon'),('2','Torre de Francotirador'),('3','Mortero'), ('4','Ballesta')], default = '1')
    damage = fields.Float()
    health = fields.Float()
    village_id = fields.Many2one('clash.village', string='Village')
    level = fields.Integer(default = 1)

    @api.constrains('level')
    def check_level(self):
        for defense in self:
            if defense.level < 1:
                raise ValidationError('The level of defense cannot be lower to 1')
            
    def button_increment_level(self):
        for defense in self:
            defense.write({'level': defense.level + 1})
        return True

    
                

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
                raise ValidationError('The number of troops cannot be lower to 1')

    @api.constrains('number_of_troops')
    def check_max_troops(self):
        for troops in self:
            if troops.camp_id.current_troops > troops.camp_id.troops_max:
                raise ValidationError('You cannot exceed the maximum limit of a camp')

class Battle(models.Model):
    _name = 'clash.battle'
    _description = 'Battle in Clash of War'

    name = fields.Char()
    player_1 = fields.Many2one('clash.player', string='Jugador 1', required=True)
    player_2 = fields.Many2one('clash.player', string='Jugador 2', required=True)
    winner = fields.Many2one('clash.player', string='Ganador', compute='_compute_ganador', store=True)
    start_date = fields.Datetime(string='Fecha de Inicio', default=fields.Datetime.now, readonly=True)
    end_date = fields.Datetime(string='Fecha de Fin', compute='_compute_end_date', store=True)
    battle_finished = fields.Boolean(string='Batalla terminada', compute='_compute_battle_finished', store=True)
    progress = fields.Float(string='Progreso', compute='_compute_progress', store=True)

    @api.constrains('player_1', 'player_2')
    def check_different_players(self):
        for battle in self:
            if battle.player_1 and battle.player_2 and battle.player_1 == battle.player_2:
                raise ValidationError('Los jugadores deben ser diferentes en una batalla.')

    @api.depends('player_1', 'player_2')
    def _compute_ganador(self):
        for batalla in self:
            if batalla.player_1 and batalla.player_2:
                diferencia_ataque = (
                    sum(tropa.damage for tropa in batalla.player_1.village_id.buildings.troops) -
                    sum(defensa.health for defensa in batalla.player_2.village_id.defenses)
                )
                diferencia_defensa = (
                    sum(defensa.damage for defensa in batalla.player_2.village_id.defenses) -
                    sum(tropa.health for tropa in batalla.player_1.village_id.buildings.troops)
                )

                if diferencia_ataque > diferencia_defensa:
                    batalla.winner = batalla.player_1
                else:
                    batalla.winner = batalla.player_2
            else:
                batalla.winner = None

    @api.depends('start_date')
    def _compute_end_date(self):
        for batalla in self:
            if batalla.start_date:
                batalla.end_date = fields.Datetime.to_string(
                    fields.Datetime.from_string(batalla.start_date) + timedelta(minutes=60)
                )

    @api.depends('start_date', 'end_date')
    def _compute_battle_finished(self):
        for batalla in self:
            if batalla.end_date and fields.Datetime.from_string(batalla.end_date) < datetime.now():
                batalla.battle_finished = True
            else:
                batalla.battle_finished = False

    @api.depends('start_date', 'end_date')
    def _compute_progress(self):
        for batalla in self:
            if batalla.start_date and batalla.end_date:
                current_time = fields.Datetime.now()
                start_datetime = fields.Datetime.from_string(batalla.start_date)
                end_datetime = fields.Datetime.from_string(batalla.end_date)
                total_time = (end_datetime - start_datetime).total_seconds() / 60
                elapsed_time = max(0, (current_time - start_datetime).total_seconds() / 60)
                progress = min(100, (elapsed_time / total_time) * 100)
                batalla.progress = progress
            else:
                batalla.progress = 0

    @api.model
    def update_battle_progress(self):
        battles = self.search([('start_date', '!=', False), ('end_date', '!=', False), ('battle_finished', '=', False)])

        for battle in battles:
            current_time = fields.Datetime.now()
            start_datetime = fields.Datetime.from_string(battle.start_date)
            end_datetime = fields.Datetime.from_string(battle.end_date)
            total_time = (end_datetime - start_datetime).total_seconds() / 60
            elapsed_time = max(0, (current_time - start_datetime).total_seconds() / 60)
            progress = min(100, (elapsed_time / total_time) * 100)
            battle._compute_battle_finished()
            battle.write({'progress': progress})



class resource_wizard(models.TransientModel):
    _name = "clash.resource_wizard"

    def _default_resource(self):
        return self._context.get('resource_context')

    name = fields.Char()
    type = fields.Selection([('1', 'Gold'), ('2', 'Mana'), ('3', 'Gems')], string='Resource Type')
    amount = fields.Integer()
    village_id = fields.Many2one('clash.village', string='Village', default=_default_resource, readonly=True)

    def launch(self):
        try:
            self.env['clash.resource'].create({'name': self.name,
                                            'type': self.type,
                                            'amount': self.amount,
                                            'village_id': self.village_id.id})
        except Exception as e:
            print("Error during resource creation:", e)


class build_wizard(models.TransientModel):
    _name = "clash.build_wizard"

    def _default_build(self):
        return self._context.get('build_context')

    name = fields.Char()
    type = fields.Selection([('1','Mina'),('2','Recolector'),('3','Extractor'),('4','Campamento')], default = '1')
    health = fields.Float()
    village_id = fields.Many2one('clash.village', string='Village', default=_default_build, readonly=True)
    troops = fields.One2many('clash.troop_type', 'camp_id')
    level = fields.Integer(default=1)

    state = fields.Selection([
        ('type', "Type Selection"),
        ('troops', "Troops Selection"),
        ('stats', "Stats Selection"),
    ], default='type')


    def button_increment_level(self):
        for builds in self:
            builds.write({'level': builds.level + 1})
        return True

    def launch(self):
        try:
            building_vals = {
                'name': self.name,
                'type': self.type,
                'health': self.health,
                'village_id': self.village_id.id,
                'level': self.level,
            }

            new_building = self.env['clash.building'].create(building_vals)

        except Exception as e:
            print("Error during build creation:", e)

    def previous(self):
        if (self.state == 'troops'):
            self.state = 'type'
        elif (self.state == 'stats'):
            self.state = 'troops'
        return {
            'type': 'ir.actions.act_window',
            'name': 'Launch build',
            'res_model': self._name,
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id,
            'context': self._context
        }

    def next(self):
        if(self.state == 'type'):
            if (self.type == '4'):
                self.state = 'troops'
            else:
                self.state = 'stats'
        elif (self.state == 'troops'):
            self.state = 'stats'
        return {
            'type': 'ir.actions.act_window',
            'name': 'Launch build',
            'res_model': self._name,
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id,
            'context': self._context
        }
    