# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta



class usuarios(models.Model):
     _name = 'res.users'
     _inherit = 'res.users'
     _description = 'proyecto.usuarios'

     login = fields.Char()
     karma = fields.Integer()
     is_premium = fields.Boolean(default = False, readonly = True)
     premium_expiry_date = fields.Date(string="Premium Expiry Date")
     days_to_expiry = fields.Integer(string="Days to Expiry", compute='_compute_days_to_expiry')


     def calcular_fecha_caducidad(self):
          # Establecer la fecha de caducidad como un mes desde hoy
          return datetime.now() + timedelta(days=30)

     @api.depends('premium_expiry_date')
     def _compute_days_to_expiry(self):
          today = fields.Date.today()
          for user in self:
               if user.premium_expiry_date:
                    expiry_date = fields.Date.from_string(user.premium_expiry_date)
                    delta = expiry_date - today
                    if delta.days < 0:
                         user.is_premium = False
                         user.days_to_expiry = 0
                    else:
                         user.days_to_expiry = delta.days
               else:
                    user.days_to_expiry = 0


class Productos(models.Model):
     _name = 'product.product'
     _inherit = 'product.product'


class Ventas(models.Model):
     _name = 'sale.order'
     _inherit = 'sale.order'

     def write(self, vals):
          res = super(Ventas, self).write(vals)
          if vals['state'] == 'sale':
               for order in self:
                    if any(line.product_id.name == 'Servicio Premium' for line in order.order_line):
                         partner = order.partner_id
                         if partner:
                              partner.user_ids.premium_expiry_date = partner.user_ids.calcular_fecha_caducidad()
                              partner.user_ids.write({'is_premium': True})
          return res
