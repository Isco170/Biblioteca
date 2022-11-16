{
 'name': "Biblioteca",
  'summary': "Gerenciar facilmente livros",
  'description':"Descricao",
  'author': "Francisco André Mavie",
  'website': "https://github.com/Isco170/Isco170",
  'category': "Tools",
  'version': '14.0.1',
  'depends': ['base'],
  'application': True,
  'sequence': 1,
  'data': [
    'security/groups.xml',
    'security/ir.model.access.csv',
    'data/data.xml',
    'views/biblioteca_livro.xml',
    'views/biblioteca_livro_categoria.xml'
  ],
  'demo': [
    'data/demo.xml',
  ],
}