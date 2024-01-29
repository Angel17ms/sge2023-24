# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student(models.Model):
    _name = 'school.student'
    _description = 'The students'

    name = fields.Char()
    year = fields.Integer()
    Fecha_De_Matriculacion = fields.Datetime()
    curso_Aprovado = fields.Boolean()
    foto = fields.Image()
    curso = fields.Selection([('1','Primero'), ('2','Segundo'), ('3', 'Tercero'), ('4','Quarto')])
    topic = fields.Many2many('school.topic')


class topic(models.Model):
    _name = 'school.topic'
    _description = 'Topics'

    name = fields.Char()
    pdf_Tema = fields.Binary()
    teacher = fields.Many2one('school.teacher')
    student = fields.Many2many('school.student')

class teacher(models.Model):
    _name = 'school.teacher'
    _description = 'The teachers'

    name = fields.Char()
    salario = fields.Float()
    topic = fields.One2many('school.topic', 'teacher')