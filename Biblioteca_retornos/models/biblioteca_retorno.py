<?xml version="1.0" encoding="utf-8" ?>
<odoo>
<!--  Book Form View inherit  -->
  <record id="biblioteca_livro_view_form_inh" model="ir.ui.view">
    <field name="name">Biblioteca Livro Form</field>
    <field name="model">biblioteca.livro</field>
    <field name="inherit_id" ref="biblioteca.biblioteca_livro_view_form"/>
    <field name="arch" type="xml">
      <field name="author_ids" position="after">
        <field name="date_return"/>
      </field>
    </field>
  </record>
  
<!--  Book Category Form View inherit  -->
  <record id="biblioteca_livro_categoria_view_form_inh" model="ir.ui.view">
    <field name="name">Biblioteca Categoria Form</field>
    <field name="model">biblioteca.livro.categoria</field>
    <field name="inherit_id" ref="biblioteca.biblioteca_livro_categoria" />
    <field name="arch" type="xml">
      <field name="parent_id" position="after">
        <field name="max_borrow_days" />
      </field>
    </field>
  </record>
</odoo>