from odoo import models, fields, api

class BibliotecaLivroRent(models.Model):
  _name = 'biblioteca.livro.rent'
  
  book_id = fields.Many2one('biblioteca.livro', 'Livro', required = True)
  borrower_id = fields.Many2one('res.partner', 'Borrower', required = True)
  state = fields.Selection([('ongoing', 'Ongoing'),
                           ('returned', 'Returned')],
                          'State', default='ongoing', required = True)
  rent_date = fields.Date(default=fields.Date.today)
  return_date = fields.Date()
  