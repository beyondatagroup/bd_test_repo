from odoo import models, fields, api

class TenderWizard(models.TransientModel):
    _name = "tender.wizard"
    _description = "Tender Process Wizard"

    name = fields.Char("Name")
    totel_gil = fields.Float("Total Time taken by GIL")
    totel_office = fields.Float("Total time taken by Dept/Office")

    tender_line_ids = fields.One2many('tender.line.wizard','tender_id')

class TenderLineWizard(models.TransientModel):
    _name = "tender.line.wizard"
    _description = "Tender Process Wizard"

    name = fields.Char("Name")
    owner = fields.Char("Owner")
    date_of_completion = fields.Date("Date of Completion")
    time_taken = fields.Char("Time Taken (Days)")

    tender_id = fields.Many2one('tender.wizard')