from odoo import http
from odoo.http import request
from odoo.tools import lazy
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute


class WebsiteSaleVisibility(WebsiteSale):

    @http.route()
    def shop(self, page=0, products=None, category=None,
             search='', ppg=False, **post):
        res = super(WebsiteSaleVisibility, self).shop(
            page=page, category=category, search=search, products=products,
            min_price=0.0, max_price=0.0, ppg=ppg, **post)
        partner = request.env['res.users'].browse(request.uid).partner_id
        product_search = request.env['product.template']
        categories = partner.category_ids
        categories_products = product_search.sudo().search(
                    [('public_categ_ids', 'child_of', categories.ids)])
        products = partner.product_ids + categories_products
        website = request.env['website'].get_current_website()
        ppr = website.shop_ppr or 4
        if not ppg:
            ppg = website.shop_ppg or 20
        pricelist = request.env['product.pricelist'].browse(
            request.session.get('website_sale_current_pl'))
        products_prices = lazy(lambda: products._get_sales_prices(pricelist))
        category = res.qcontext['category']
        if not products:
            if not categories:
                return res
            products = categories_products
        if category and categories:
            products = product_search.sudo().search(
                [('public_categ_ids', 'child_of', category.ids),
                 ('id', 'in', products.ids)])
        print(len(products))
        print(ppg)
        if len(products) <= ppg:
            res.qcontext['pager'].update({'page_count': 1})
        res.qcontext.update({
            'categories': categories,
            'products': products,
            'bins': lazy(
                lambda: TableCompute().process(products, ppg, ppr)),
            'pricelist': pricelist,
            'products_prices': products_prices,
            'get_product_prices': lambda product: lazy(
                lambda: products_prices[product.id])
        })
        return res
