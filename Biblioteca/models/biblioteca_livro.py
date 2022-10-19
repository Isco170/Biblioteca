from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
from datetime import timedelta

class BaseArchive(models.AbstractModel):
  _name = 'base.archive'
  _description = "Abstract Archive"
  
  active = fields.Boolean(default=True)
  
  def do_archive(self):
    for record in self:
      record.active = not record.active
      
class BibliotecaLivro(models.Model):
  _name = 'biblioteca.livro'
  _inherit = ['base.archive']
  _description = 'Biblioteca Livro'
  _order = 'date_release desc, name'
  _rec_name = 'abreviatura'
  manager_remarks = fields.Text('Manager Remarks')
  abreviatura = fields.Char('Short Title', required=True)
  notes = fields.Text('Internal Notes')
  description = fields.Html('Description')
  cover = fields.Binary('Book Cover')
  out_of_print = fields.Boolean('Out of Print?')
  name = fields.Char('Title', required=True)
  isbn = fields.Char('ISBN')
  old_edition = fields.Many2one('biblioteca.livro', string = 'Velha Edição')
  date_release = fields.Date('Release Date')
  date_updated = fields.Datetime('Last Updated')
  pages = fields.Integer('Number of Pages')
  age_days = fields.Float(
    string = 'Days Since Release',
    compute = '_compute_age',
    inverse = '_inverse_age',
    search ='search_age',
    store = False, # optional
    compute_sudo = True # optional
  )
  reader_rating = fields.Float('Reader Avarege Rating', digits = (14, 4),)
  cost_price = fields.Float('Livro Custo', digits = 'Livro Preco')
  currency_id = fields.Many2one('res.currency', string='Currency')
  
  retail_price = fields.Monetary(
    'Retail Price',
#     optional: currency_field = 'currency_id',
  )
  author_ids = fields.Many2many('res.partner', string = 'Authors')
  
  publisher_id = fields.Many2one(
    'res.partner', string = 'Publisher',
#     Optional:
    ondelete = 'set null',
    context= {},
    domain = [],
  )
  
  publisher_city = fields.Char(
    'Publisher City',
    related = 'publisher_id.city',
    readonly = True)
  
  category_id = fields.Many2one('biblioteca.livro.categoria')
  
  ref_doc_id = fields.Reference(
    selection = '_referencable_models',
    string = 'Reference Document'
  )
  
  state = fields.Selection([
    ('draft', 'Unavailable'),
    ('available', 'Available'),
    ('borrowed', 'Borrowed'),
    ('lost', 'Lost')],
    'State', default="draft")
  
  _sql_constraints = [
    ('name_uniq', 'UNIQUE (name)','O titulo do livro deve ser unico.'),
    ('positive_page', 'CHECK(pages>0)','Nr de paginas deve ser positivo')
  ]
  
  @api.constrains('date_release')
  def _check_release_date(self):
    for record in self:
      if record.date_release and record.date_release > fields.Date.today():
        raise models.ValidationError(
        'Release date must be in the past')
  
  def _inverse_age(self):
    today = fields.Date.today()
    for book in self.filtered('date_release'):
      d = today = timedelta(days=book.age_days)
      bool.date_release = d
  
  def _search_age(self, operator, value):
    today = fields.Date.today()
    value_days = timedelta(days=value)
    value_date = today - value_days
#     Convert the operator:
# book with age > value have a date <value_date
    operator_map = {
      '>': '<', '>=': '<=',
      '<': '>', '<=': '>=',
    }
    
    new_op = operator_map.get(operator, operator)
    return [('date_release',new_op, value_date)]
  
  @api.depends('date_release')
  def _compute_age(self):
    today = fields.Date.today()
    for book in self:
      if book.date_release:
        delta = today - book.date_release
        book.age_days = delta.days
      else:
        book.age_days = 0
  
  @api.model
  def _referencable_models(self):
    models = self.env['ir.model'].search([
      ('field_id.name', '=', 'message_ids')])
    return [(x.model, x.name) for x in models]
  
#   Helper method to check whether a state transition is allowed
  @api.model
  def is_allowed_transition(self, old_state, new_state):
    allowed = [('draft', 'available'),
               ('available', 'borrowed'),
               ('borrowed', 'available'),
               ('available', 'lost'),
               ('borrowed', 'lost'),
               ('lost', 'available')]
    return (old_state, new_state) in allowed
  
#   Method to change the state of some books to new state
  def change_state(self, new_state):
    for book in self:
      if book.is_allowed_transition(book.state, new_state):
        book.state = new_state
      else:
        msg = _('Moving from %s to %s is not allowed') % (book.state, new_state)
        raise UserError(msg)
  
#   Method to change the book state by calling the change_state method
  def make_available(self):
    self.change_state('available')
  
  def make_borrowed(self):
    self.change_state('borrowed')
    
  def make_lost(self):
    self.change_state('lost')
    
  def log_all_library_members(self):
#     This is an empty recordset of model biblioteca.membro
    biblioteca_membro_model = self.env['biblioteca.membro']
    all_members = biblioteca_membro_model.search([])
    print("ALL MEMBERS: ", all_members)
    return True
  
  def change_release_date(self):
    self.ensure_one()
    self.date_release = fields.Date.today()
    
  def find_book(self):
    domain = [
      '|',
      '&', ('name', 'ilike', 'Book Name'),
          ('category_id.name', 'ilike', 'Category Name'),
      '&', ('name', 'ilike', 'Book Name 2'),
          ('category_id.name', 'ilike', 'Category Name 2')
    ]
    
    books = self.search(domain)
    
  @api.model
  def get_author_names(self, books):
    return books.mapped('author_ids.name')
#   @api.model
#   def books_with_multiple_authors(self, all_books):
  
#   def predicate(book):
#     if len(book.author_ids) > 1:
#       return True
#     return False

#   Extend create()
  @api.model
  def create(self, values):
    if not self.user_has_groups('my_library.acl_book_librarian'):
       if 'manager_remarks' in values:
         raise UserError('You are not allowed to modify ' 'manager_remarks')
    return super(BibliotecaLivro, self).create(values)
    
  @api.model
  def write(self, values):
    if not sel.user_has_groups('my_library.acl_book_librarian'):
      if 'manager_remarks' in values:
        raise UserError('You are not allowed to modify ' 'manager_remarks')
    return super(BibliotecaLivro, self).write(values)
  
  def name_get(self):
    result = []
    for book in self:
      authors = book.author_ids.mapped('name')
      name = '%s (%s)' % (book.name, ', '.join(authors))
      result.append((book.id, name))
      return result
  
  def _name_search(self, name='', args =None, operator='ilike', limit = 100, name_get_uid=None):
    args = [] if args is None else args.copy()
    if not(name == '' and operator == 'ilike'):
      args += ['|', '|',
               ('name', operator, name),
               ('isbn', operator, name),
               ('author_ids.name', operator, name)
              ]
      return super(BibliotecaLivro, self)._name_search(
        name = name, args = args, operator = operator, limit = limit, name_get_uid = name_get_uid)
    
  @api.model
  def _get_average_cost(self):
    grouped_result = self.read_group(
      [('cost_price', "!=", False)], # Domain
      ['categoria_id', 'cost_price:avg'], # Fields to access
      ['categoria_id'] # group_by
    )
    return grouped_result
    
class ResPartner(models.Model):
  _inherit = 'res.partner'
  _order = 'name'
  
  published_book_ids = fields.One2many(
    'biblioteca.livro', 'publisher_id',
    string = 'Published Books')
  
  authored_books_ids = fields.Many2many(
    'biblioteca.livro',
    string = 'Authored Books',
#     relation = 'biblioteca_book_res_partner_rel'
#     optional
  )
  count_books = fields.Integer('Number of authored Books',
                              compute = '_compute_count_books')
  
  @api.depends('authored_books_ids')
  def _compute_count_books(self):
    for r in self:
      r.count_books = len(r.authored_books_ids)
      
class LibraryMember(models.Model):
  _name = 'biblioteca.membro'
  _description = 'Descricao'
  _inherits = {'res.partner': 'partner_id'}
  partner_id = fields.Many2one(
    'res.partner',
    ondelete = 'cascade',
    required=True
  )
  
  date_start = fields.Date('Member Since')
  date_end = fields.Date('Termination Date')
  member_number = fields.Char()
  date_of_birth = fields.Date('Date of birth')
  