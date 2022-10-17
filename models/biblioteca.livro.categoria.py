from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LivroCategoria(models.Model):
  _name = 'biblioteca.livro.categoria'
  _description = 'Biblioteca Livro Categoria'
  _parent_store = True
  _parent_name = "parent_id"  # optional if field is 'parent_id'

  name = fields.Char('Categoria')
  description = fields.Text('Description')
  parent_id = fields.Many2one(
    'biblioteca.livro.categoria',
    string = 'Parent Category',
    ondelete = 'restrict',
    index = True
  )
  
  child_ids = fields.One2many(
    'biblioteca.livro.categoria', 'parent_id',
    string = 'Child Categories')
  parent_path = fields.Char(index=True)
  
  def _check_hierarchy(self):
    if not self._check_recursion():
      raise models.ValidationError(
        'Error! You cannot create recursive categories.')
  
  def create_categories(self):
    categ1 = {
      'name': 'Child category 1',
      'description': 'Description for child 1'
    }