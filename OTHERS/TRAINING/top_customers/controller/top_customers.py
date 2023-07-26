""" top10 customers  """
from odoo import http
from odoo.http import request


class TopCustomers(http.Controller):
    """ controller class for snippet """

    @http.route(['/top_customers'], type="json", auth="public")
    def sold_total(self):
        """ controller method for showing dynamic snippet
            passes top 10 customer details """
        top10 = []
        for rec in request.env['sale.order'].search([]).mapped(
                'partner_id').ids:
            image = request.env['res.partner'].browse(rec).image_1920
            if not image:
                image = request.env['res.partner'].browse(rec).avatar_128
            top10.append({
                'id': rec,
                'partner': request.env['res.partner'].browse(rec).name,
                'image': image,
                'count': request.env['sale.order'].search_count(
                    [('partner_id', '=', rec)]),
            })
        top10 = sorted(top10, key=lambda i: i['count'], reverse=True)[:10]
        return top10

    @http.route('/top_customers/<model("res.partner"):partner>', type='http',
                auth="user", website=True)
    def product_details(self, partner):
        """ controller method for each customer details
            using dynamic routes """
        return request.render(
            'top_customers.customer_details', {'partner': partner})
