from odoo import models, fields, api

class BibliotecaLivro(models.Model):
  _inherit = 'biblioteca.livro'
  
  date_return = fields.Date('Data retorno')
  
  def make_borrowed(self):
    day_to_borrow = self.categoria_id.max_borrow_days or 10
    self.date_return = fields.Date.today() + timedelta(days = day_to_borrow)
    return super(BibliotecaLivro, self).make_borrowed()
  
  def make_available(self):
    self.date_return = False
    return super(BibliotecaLivra, self).make_available()
  
class BibliotecaLivroCategoria(models.Model):
  _inherit = 'biblioteca.livro.categoria'
  
  max_borrow_days = fields.Integer(
    'Maximo dias emprestado',
    help = "Por quantos dias o livro pode ser emprestado",
    default = 10)