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
  cost_price = fields.Float(
    'Livro Custo', digits = 'Livro Preco'
  )
  currency_id = fields.Many2one(
    'res.currency', string='Currency')
  
  retail_price = fields.Monetary(
    'Retail Price',
#     optional: currency_field = 'currency_id',
  )
  author_ids = fields.Many2many(
    'res.partner',
    string = 'Authors'
  )
  
  publisher_id = fields.Many2one(
    'res.partner', string = 'Publisher',
#     Optional:
    ondelete = 'set null',
    context= {},
    domain = [],
  )
  
  category_id = fields.Many2one('biblioteca.livro.categoria')
  
class ResPartner(models.Model):
  _inherit = 'res.partner'
  published_book_ids = fields.One2many(
    'biblioteca.livro', 'publisher_id',
    string = 'Published Books')
  
  authored_books_ids = fields.Many2many(
    'biblioteca.livro',
    string = 'Authored Books',
#     relation = 'biblioteca_book_res_partner_rel'
#     optional
  )