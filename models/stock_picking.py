# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api,fields, models,  _
from odoo.exceptions import UserError, ValidationError
import logging


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    usuario_normal = fields.Boolean(compute='_compute_usuario_normal')
    
    def _compute_show_validate(self):
        for picking in self:
            if not self.user_has_groups('stock.group_stock_manager') and self.env.user.default_location_id.id != self.location_dest_id.id:
                picking.show_validate = False
                return
                
        res = super(StockPicking, self)._compute_show_validate()
    
    @api.depends('picking_type_id')
    def _compute_usuario_normal(self):
        for record in self:
            record.usuario_normal = not self.user_has_groups('stock.group_stock_manager')

    def button_validate(self):
        usuario_inventario = self.user_has_groups('stock.group_stock_user')
        responsable_inventario = self.user_has_groups('stock.group_stock_manager')

        if usuario_inventario and not responsable_inventario:
            if self.picking_type_id.code == 'internal':
                for l in self.move_line_ids_without_package:
                    if l.lot_id and l.lot_id.name:
                        quants = self.env['stock.quant'].search([('lot_id', '=', l.lot_id.id), ('location_id','=',l.location_id.id), ('product_id','=',l.product_id.id), ('quantity','>=',1)])
                        if not quants:
                            raise UserError('La serie {} no existe en la ubicación de origen'.format(l.lot_id.name))

        res = super(StockPicking, self).button_validate()
