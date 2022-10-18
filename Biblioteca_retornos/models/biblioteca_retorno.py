from odoo import models, fields, api

class BibliotecaLivro(models.Model):
  _inherit = 'biblioteca.livro'
  
  date_return = fields.Date('Data retorno')
  
class BibliotecaLivroCategoria(models.Model):
  _inherit = 'biblioteca.livro.categoria'
  
  max_borrow_days = fields.Integer(
    'Maximo dias emprestado',
    help = "Por quantos dias o livro pode ser emprestado",
    default = 10)