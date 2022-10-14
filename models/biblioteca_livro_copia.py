from odoo import models, fields, api

class BibliotecaLivroCopia(models.Model):
  _name = 'biblioteca.livro.copia'
  _inherit = 'biblioteca.livro'
  _description = 'Biblioteca Livros Copia'