from odoo import models, fields
class BibliotecaLivro(models.Model):
  _name = 'biblioteca.livro'
  _description = 'Biblioteca Livro'
  _order = 'date_release desc, name'
  _rec_name = 'abreviatura'
  abreviatura = fields.Char('Short Title', required=True)
  notes = fields.Text('Internal Notes')
  state = fields.Selection(
  [('draft', 'Not Available'),
   ('available', 'Available'),
   ('lost', 'Lost')],
    'State')
  description = fields.Html('Description')
  cover = fields.Binary('Book Cover')
  out_of_print = fields.Boolean('Out of Print?')
  name = fields.Char('Title', required=True)
  date_release = fields.Date('Release Date')
  date_updated = fields.Datetime('Last Updated')
  pages = fields.Integer('Number of Pages')
  reader_rating = fields.Float(
    'Reader Avarege Rating', 
    digits = (14, 4),
  )
  author_ids = fields.Many2many(
    'res.partner',
    string = 'Authors'
  )