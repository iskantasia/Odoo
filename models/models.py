# -*- coding: utf-8 -*-

from odoo import models, fields, api

class type_request(models.Model) :
    _name = 'purchasing.type_request'
    _description = 'purchasing.type_request'
    _rec_name = 'type'

    type = fields.Char()

class form_stationery(models.Model):
    _name = 'purchasing.stationery'
    _description = 'purchasing.stationery'

    kode_barang = fields.Char()
    nama_barang = fields.Char()
    jumlah_permintaan = fields.Integer()
    jumlah_realisasi = fields.Integer()
    keterangan = fields.Char()
    perusahaan = fields.Selection([('K', 'Kawasan Industri Jababeka'), ('I', 'Indocargomas Persada'), (
        'G', 'Grahabuana Cikarang'), ('B', 'Bekasi Power'), ('M', 'Metropark Condominium Indah')], default='K')
    jenis_permintaan = fields.Many2many('purchasing.type_request', string = "Jenis Permintaan")
    dikeluarkan =  fields.Char(compute='_get_user')
    diterima = fields.Char()
    disetujui = fields.Char()
    Pemohon = fields.Char()

    def _get_user(self) :
        self.dikeluarkan = self.env.user.email
    
    def approve(self) :
        self.diterima = self.env.user.email
        return {
          "type": "ir.actions.act_window",
          "view_mode": "tree,form",
          "res_model": "purchasing.stationery",
        }