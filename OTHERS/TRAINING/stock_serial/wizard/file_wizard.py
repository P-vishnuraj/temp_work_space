import base64

from odoo import fields, models, _
from odoo import exceptions
import openpyxl
import base64
from io import BytesIO


class FileWizard(models.TransientModel):
    _name = 'file.wizard'
    _description = 'Test Model Wizard'

    file_lot = fields.Binary(string='Choose file')

    def action_upload(self):
        """ action method for import excel sheet data... """
        fail_flag = 0
        succ_flag = 0
        try:
            wb = openpyxl.load_workbook(
                filename=BytesIO(base64.b64decode(self.file_lot)), read_only=True
            )
            ws = wb.active

        except OSError as exc:
            if exc.errno == 36:
                raise exceptions.UserError('filename too long.')
        except FileNotFoundError:
            raise exceptions.UserError('No such file or directory found. \n%s.' % self.file_lot)
        except:
            raise exceptions.UserError('Only excel files are supported.')
        for record in ws.iter_rows(min_row=2, max_row=None, min_col=None, max_col=None, values_only=True):
            if record[0] and record[2]:
                succ_flag += 1
                p_name = str(record[2]).split(" ")[0].replace("[", "").replace("]", "")  # split here....
                p_id = self.env['product.product'].search([('default_code', '=', p_name)]).id
                self.env['stock.lot'].create({
                    'name': record[0],
                    'product_id': p_id,
                    'company_id': self.env.company.id,
                })
                print(record[0], ":", p_id, ":", self.env.company.id)
            if (record[0] and not record[2]) or (not record[0] and record[2]):
                fail_flag += 1
        if fail_flag:
            raise exceptions.UserError('%d records are not added because they dont have both lot/serial number and '
                                       'product name' % fail_flag)

        # raise exceptions.UserError('%d records are successfully added' % succ_flag)

