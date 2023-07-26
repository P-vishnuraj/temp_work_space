import xmlrpc.client
from datetime import date
from odoo import fields, models


class MigratePurchase(models.TransientModel):
    """ Model for do purchase order migration from odoo15 DB to odoo16 DB """
    _name = 'migrate.purchase'
    _description = 'Purchase Order Migration'

    def _current_db(self):
        """ Method to take current db name  """
        return self._cr.dbname

    def _current_username(self):
        """ Method to take current username """
        return self.env.user.login

    url_from = fields.Char("Url of 1st DB")
    url_to = fields.Char("Url of 2nd DB", default="http://localhost:8016")
    database_from = fields.Char("Database to take")
    database_to = fields.Char("Database to migrate", default=_current_db)
    username_from = fields.Char("Username of 1st DB")
    username_to = fields.Char("Username of 2nd DB", default=_current_username)
    password_from = fields.Char("Password")
    password_to = fields.Char("Password", default=1)

    def action_migrate_records(self):
        """ Action method to migrate records from DB_v15 to DB_v16 """
        url_db1 = self.url_from             #URL of first DataBase
        db_1 = self.database_from           #First Database name
        username_db_1 = self.username_from  #First Database username
        password_db_1 = self.password_from  #First Database password
        url_db2 = self.url_to               #URL of second DataBase
        db_2 = self.database_to             #Second Database name
        username_db_2 = self.username_from  #Second Database username
        password_db_2 = self.password_to    #Second Database password
        common_1 = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(url_db1))
        models_1 = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/object'.format(url_db1))
        version_db1 = common_1.version()
        common_2 = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(url_db2))
        models_2 = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/object'.format(url_db2))
        version_db2 = common_2.version()
        uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
        uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})
        db_1_orders = models_1.execute_kw(
            db_1, uid_db1, password_db_1, 'purchase.order', 'search_read', [[]],
            {'fields': ['partner_id', 'order_line']})
        db_1_lines = models_1.execute_kw(
            db_1, uid_db1, password_db_1, 'purchase.order.line', 'search_read',
            [[]], {'fields': ['order_id', 'product_id']})

        total_orders = 0
        for record in db_1_orders:
            total_orders += 1
            order_id = record["id"]
            del record["id"]
            del record["order_line"]
            record.update({"partner_id": record["partner_id"][0]})
            new_record = models_2.execute_kw(db_2, uid_db2, password_db_2,
                                             'purchase.order', 'create',
                                             [record])
            for line in db_1_lines:
                if order_id == line["order_id"][0]:
                    try:
                        product_name = line["product_id"][1].split("]")[
                            1].strip()
                    except:
                        product_name = line["product_id"][1]
                    db_2_products = models_2.execute_kw(
                        db_2, uid_db2, password_db_2, 'product.product',
                        'search_read', [[['name', '=', product_name]]],
                        {'fields': ['name']})
                    # Taking copy of order line to avoid error in looping
                    build_line = line.copy()
                    build_line.update({"product_id": db_2_products[0]["id"]})
                    build_line.update({"order_id": new_record})
                    del build_line["id"]
                    models_2.execute_kw(db_2, uid_db2, password_db_2,
                                        'purchase.order.line', 'create',
                                        [build_line])
        self.env['migration.details'].create({
            'data': "Purchase Orders",
            'database_from': db_1,
            'database_to': db_2,
            'count': total_orders,
            'user': self.env.user.partner_id.name,
            'date': date.today()
        })
        return {
            'effect': {
                'fadeout': 'slow',
                'message': f"Total %s Purchase Orders Migrated" % total_orders,
                'type': 'rainbow_man',
            }
        }
