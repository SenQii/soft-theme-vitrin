#!/usr/bin/env python3
"""
Local development server for Zid Jinja2 theme
Run with: python server.py
"""

from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime
from jinja2 import nodes
from jinja2.ext import Extension

# Custom Zid extension for all Zid tags
class ZidExtension(Extension):
    tags = set(['template_components', 'section_components', 'vitrin_head', 'vitrin_body'])
    
    def parse(self, parser):
        lineno = next(parser.stream).lineno
        tag_name = parser.stream.current.value
        
        if tag_name == 'template_components':
            # Render sample sections for home page
            return nodes.Output([
                nodes.TemplateData('''
                {% include 'sections/main-slider.jinja' %}
                {% include 'sections/features-section.jinja' %}
                {% include 'sections/products-section.jinja' %}
                {% include 'sections/category-section.jinja' %}
                {% include 'sections/testimonials.jinja' %}
                ''')
            ], lineno=lineno)
        
        elif tag_name == 'vitrin_head':
            # Add essential head tags for Zid
            return nodes.Output([
                nodes.TemplateData('''
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <meta name="description" content="Zid Theme Preview">
                <title>{{ store.name }} - Zid Theme</title>
                ''')
            ], lineno=lineno)
        
        elif tag_name == 'vitrin_body':
            # Add body attributes for Zid
            return nodes.Output([
                nodes.TemplateData(' class="zid-theme rtl" dir="rtl"')
            ], lineno=lineno)
        
        elif tag_name == 'section_components':
            return nodes.Output([nodes.TemplateData('')], lineno=lineno)
        
        return nodes.Output([nodes.TemplateData('')], lineno=lineno)

app = Flask(__name__, 
           template_folder='.', 
           static_folder='assets',
           static_url_path='/assets')

# Set secret key for sessions
app.secret_key = 'dev-secret-key-for-local-testing'

# Configure Jinja2
app.jinja_env.add_extension('jinja2.ext.i18n')
app.jinja_env.add_extension(ZidExtension)

# Handle vitrin: namespace templates
from jinja2 import TemplateNotFound

def vitrin_template_loader(environment, template):
    if template.startswith('vitrin:'):
        # Convert vitrin:path/file.jinja to vitrin/path/file.jinja
        local_template = template.replace('vitrin:', 'vitrin/')
        try:
            return environment.get_template(local_template)
        except TemplateNotFound:
            # Return empty template if vitrin template doesn't exist
            return environment.from_string('<!-- Vitrin template placeholder: {{ template }} -->')
    return None

# Monkey patch the template loading
original_get_template = app.jinja_env.get_template

def patched_get_template(name, parent=None, globals=None):
    if name.startswith('vitrin:'):
        local_name = name.replace('vitrin:', 'vitrin/')
        try:
            return original_get_template(local_name, parent, globals)
        except TemplateNotFound:
            return app.jinja_env.from_string('<!-- Vitrin template: ' + name + ' -->')
    return original_get_template(name, parent, globals)

app.jinja_env.get_template = patched_get_template

# Helper classes
class MockLocale:
    def __init__(self, language='ar'):
        self.language = language
        self.code = language
        self.direction = 'rtl' if language == 'ar' else 'ltr'

class MenuContainer:
    """Container for menu items that avoids dict.items() conflict"""
    def __init__(self, menu_items):
        self.items = menu_items

class MenuItem:
    """Menu item object that avoids dict.items() conflict"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# Create comprehensive mock data for all templates
SAMPLE_DATA = {
    'store': {
        'name': 'متجر الأناقة الناعمة',
        'name_en': 'Soft Elegance Store',
        'logo': '/assets/zid-logo.svg',
        'icon': '/assets/zid-logo.svg',
        'permalink': 'https://store.zid.sa/',
        'editing_mode': False,
        'language': 'ar',
        'currency': {'code': 'SAR', 'symbol': 'ر.س', 'name': 'Saudi Riyal'},
        'rtl': True,
        'countries': [{'id': 1, 'name': 'المملكة العربية السعودية'}],
        'languages': [{'code': 'ar', 'name': 'العربية'}],
        'settings': {
            'branding': {
                'colors': {
                    'primary': '#6D192B',
                    'on_primary': '#FFFFFF',
                },
                'mobile_app_logo': '/assets/zid-logo.svg',
                'copyrights': '© 2024 متجر الأناقة الناعمة'
            },
            'general': {
                'availability': {'closed_now': False},
                'business_address': {
                    'show_location': True,
                    'street': 'شارع الملك فهد',
                    'city': {'name': 'الرياض', 'country': {'name': 'المملكة العربية السعودية'}},
                    'district': 'العليا',
                    'latitude': '24.7136',
                    'longitude': '46.6753'
                },
                'tax_settings': {
                    'tax_percentage_formatted': '15%',
                    'is_certificate_visible': True,
                    'tax_registration_certificate': '/assets/vat-certificate.png',
                    'tax_number': '123456789'
                },
                'commercial_registration_number': '123456789',
                'one_signal': {
                    'ios_app_id': '123456789',
                    'android_package_name': 'com.store.app'
                }
            },
            'contact': {
                'phone': '+966501234567',
                'email': 'info@store.com',
                'website': 'https://store.com',
                'facebook': 'storepage',
                'instagram': 'storepage',
                'twitter': 'storepage'
            },
            'products': {
                'wishlist_enabled': True,
                'reviews_enabled': True,
                'questions_enabled': True
            },
            'checkout': {
                'is_loyalty_enabled': True,
                'shipping_methods': [
                    {'id': 1, 'name': 'توصيل سريع', 'icon': '/assets/zidship.svg'}
                ],
                'payment_methods': [
                    {'id': 1, 'name': 'فيزا', 'icon': '/assets/visa.svg'},
                    {'id': 2, 'name': 'ماستركارد', 'icon': '/assets/mastercard.svg'}
                ],
                'gift_order_settings': {
                    'is_gift_order_enabled': '1',
                    'is_gift_order_customer_motivation_enabled': '1'
                }
            },
            'menus': {
                'main_menu': MenuContainer([
                    MenuItem(label='الرئيسية', url='/', slug='home', resource_type='page', items=[]),
                    MenuItem(label='الأزياء', url='/categories/1/fashion', slug='fashion', resource_type='category', items=[]),
                    MenuItem(label='العطور', url='/categories/2/perfumes', slug='perfumes', resource_type='category', items=[])
                ])
            }
        }
    },
    'products': {
        'results': [
            {
                'id': '1',
                'slug': 'elegant-dress',
                'name': 'فستان أنيق',
                'description': 'فستان أنيق ومريح للمناسبات الخاصة',
                'html_url': 'http://localhost:8000/product/1',
                'main_image': {
                    'image': {
                        'small': '/assets/woman.png',
                        'medium': '/assets/woman.png',
                        'full_size': '/assets/woman.png'
                    },
                    'alt_text': 'فستان أنيق'
                },
                'images': [{'image': {'small': '/assets/woman.png', 'medium': '/assets/woman.png', 'full_size': '/assets/woman.png'}, 'alt_text': 'فستان أنيق'}],
                'formatted_price': '299.00 ر.س',
                'formatted_sale_price': None,
                'in_stock': True,
                'quantity': 50,
                'is_infinite': False,
                'rating': {'average': 4.5, 'total_count': 25},
                'selected_product': {
                    'id': '1', 
                    'formatted_price': '299.00 ر.س', 
                    'in_stock': True,
                    'quantity': 50,
                    'is_infinite': False
                }
            },
            {
                'id': '2',
                'name': 'عطر فاخر',
                'main_image': {'image': {'small': '/assets/perfoum.png', 'medium': '/assets/perfoum.png', 'full_size': '/assets/perfoum.png'}},
                'formatted_price': '450.00 ر.س',
                'in_stock': True,
                'quantity': 25,
                'is_infinite': False,
                'rating': {'average': 5.0, 'total_count': 15}
            }
        ],
        'count': 2
    },
    'categories': [
        {
            'id': '1', 
            'name': 'الأزياء', 
            'slug': 'fashion',
            'url': '/categories/1/fashion',
            'description': 'أحدث صيحات الموضة والأزياء',
            'image': '/assets/woman.png',
            'sub_categories': [],
            'parent_category': None
        },
        {
            'id': '2', 
            'name': 'العطور', 
            'slug': 'perfumes',
            'url': '/categories/2/perfumes',
            'description': 'أفخم أنواع العطور والروائح',
            'image': '/assets/perfoum.png',
            'sub_categories': [],
            'parent_category': None
        }
    ],
    'cart': {
        'products_count': 0,
        'totals': [
            {'code': 'subtotal', 'title': 'المجموع الفرعي', 'value_string': '0.00 ر.س'},
            {'code': 'total', 'title': 'المجموع', 'value_string': '0.00 ر.س'}
        ],
        'free_shipping_rule': {
            'code': 'FREE_SHIPPING',
            'subtotal_condition': {
                'status': 'min_not_reached',
                'remaining_to_min_total': '75.00 ر.س',
                'min_total': '400.00 ر.س',
                'max_total': '1000.00 ر.س',
                'products_subtotal_percentage_from_min': 75
            },
            'shipping_cities_condition': [
                {'name': 'الرياض'},
                {'name': 'جدة'}
            ]
        },
        'coupon': None,
        'gift_card_details': None,
        'currency': {
            'cart_currency': {'code': 'SAR', 'symbol': 'ر.س'}
        }
    },
    'settings': {
        'header_logo': '/assets/zid-logo.svg',
        'header_logo_mobile': '/assets/zid-logo.svg',
        'header_search_placeholder': 'ابحث هنا...',
        'header_options': [],
        'fonts_name': 'Cairo',
        'colors_header_background_color': '#D5A1AD',
        'title': 'المنتجات المميزة',
        'more_text': 'عرض جميع المنتجات',
        'products': {
            'results': [
                {
                    'id': '1',
                    'slug': 'elegant-dress',
                    'name': 'فستان أنيق',
                    'description': 'فستان أنيق ومريح للمناسبات الخاصة',
                    'html_url': 'http://localhost:8000/product/1',
                    'main_image': {
                        'image': {
                            'small': '/assets/woman.png',
                            'medium': '/assets/woman.png',
                            'full_size': '/assets/woman.png'
                        },
                        'alt_text': 'فستان أنيق'
                    },
                    'formatted_price': '299.00 ر.س',
                    'in_stock': True,
                    'rating': {'average': 4.5, 'total_count': 25}
                },
                {
                    'id': '2',
                    'slug': 'luxury-perfume',
                    'name': 'عطر فاخر',
                    'description': 'عطر فاخر برائحة مميزة',
                    'html_url': 'http://localhost:8000/product/2',
                    'main_image': {
                        'image': {
                            'small': '/assets/perfoum.png',
                            'medium': '/assets/perfoum.png',
                            'full_size': '/assets/perfoum.png'
                        },
                        'alt_text': 'عطر فاخر'
                    },
                    'formatted_price': '450.00 ر.س',
                    'in_stock': True,
                    'rating': {'average': 5.0, 'total_count': 15}
                }
            ],
            'url': '/products'
        }
    },
    'customer': None,
    'orders': {'results': []},
    'addresses': []
}

@app.before_request
def setup_session():
    """Setup session data for all requests"""
    session['locale'] = 'ar'
    session['currency'] = 'SAR'
    session['user_id'] = None
    session['template'] = 'home'  # Add template context

@app.route('/')
def home():
    return render_template('templates/home.jinja', **SAMPLE_DATA)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in SAMPLE_DATA['products'] if p['id'] == product_id), None)
    if not product:
        return render_template('templates/404_not_found.jinja', **SAMPLE_DATA)
    
    data = SAMPLE_DATA.copy()
    data['product'] = product
    return render_template('templates/product.jinja', **data)

@app.route('/category/<int:category_id>')
def category(category_id):
    category_data = next((c for c in SAMPLE_DATA['categories'] if int(c['id']) == category_id), None)
    if not category_data:
        return render_template('templates/404_not_found.jinja', **SAMPLE_DATA)
    
    data = SAMPLE_DATA.copy()
    data['category'] = category_data
    
    # Create products data with pagination info for category page
    data['products'] = {
        'results': SAMPLE_DATA['products']['results'],
        'count': SAMPLE_DATA['products']['count'],
        'page': 1,
        'pages_count': 1,
        'filters': [],
        'data': SAMPLE_DATA['products']['results']
    }
    return render_template('templates/category.jinja', **data)

@app.route('/cart_page')
def cart_page():
    return render_template('templates/cart.jinja', **SAMPLE_DATA)



@app.route('/search')
def search():
    query = request.args.get('q', '')
    data = SAMPLE_DATA.copy()
    data['search_query'] = query
    data['search_results'] = SAMPLE_DATA['products'] if query else []
    return render_template('templates/search.jinja', **data)

@app.route('/account/profile')
def profile():
    data = SAMPLE_DATA.copy()
    data['user'] = {
        'name': 'أحمد محمد',
        'email': 'ahmed@example.com',
        'phone': '+966501234567'
    }
    return render_template('templates/account_profile.jinja', **data)



@app.route('/account/orders')
def account_orders():
    data = SAMPLE_DATA.copy()
    data['user'] = {
        'name': 'أحمد محمد',
        'orders': []
    }
    return render_template('templates/account_orders.jinja', **data)

@app.route('/account/addresses')
def account_addresses():
    data = SAMPLE_DATA.copy()
    data['user'] = {
        'name': 'أحمد محمد',
        'addresses': []
    }
    return render_template('templates/account_addresses.jinja', **data)

@app.route('/account/wishlist')
def account_wishlist():
    data = SAMPLE_DATA.copy()
    data['user'] = {
        'name': 'أحمد محمد'
    }
    data['wishlist_products'] = []
    return render_template('templates/account_wishlist.jinja', **data)

@app.route('/shipping-payment')
def shipping_payment():
    return render_template('templates/shipping_payment.jinja', **SAMPLE_DATA)

# Add missing routes for url_for
@app.route('/products')
def list_products():
    return render_template('templates/products.jinja', **SAMPLE_DATA)

@app.route('/categories/<category_id>/<slug>')
def category_details(category_id, slug):
    return category(int(category_id))

@app.route('/categories/<int:category_id>')
def category_by_id(category_id):
    return category(category_id)

@app.route('/profile')
def profile_page():
    return profile()

@app.route('/login')
def login_page():
    return render_template('templates/account_profile.jinja', **SAMPLE_DATA)

@app.route('/product/<slug>/questions')
def product_questions(slug):
    # Mock product questions page
    data = SAMPLE_DATA.copy()
    data['product'] = next((p for p in SAMPLE_DATA['products']['results'] if p['slug'] == slug), SAMPLE_DATA['products']['results'][0])
    data['product']['questions'] = {'page': 1, 'pages_count': 1, 'results': []}
    return render_template('templates/questions.jinja', **data)

# Add filters for template compatibility
@app.template_filter('asset_url')
def asset_url(filename):
    return f'/assets/{filename}'

@app.template_filter('image_url')
def image_url(image_path, size=None):
    if not image_path:
        return '/assets/woman.png'  # default image
    if image_path.startswith('/assets'):
        return image_path
    return f'/assets/{image_path}'

@app.template_filter('money')
def money_filter(amount):
    return f'{amount:.2f} ر.س'

@app.template_filter('t')
def translate_filter(key):
    # Simple translation fallback
    translations = {
        'Search': 'بحث',
        'Cart': 'السلة',
        'Wishlist': 'المفضلة',
        'Account': 'الحساب',
        'Home': 'الرئيسية'
    }
    return translations.get(key, key)

@app.template_filter('localized_url')
def localized_url_filter(path):
    # For local development, just return the path as-is
    if not path:
        return '/'
    return path if path.startswith('/') else f'/{path}'

# Add i18n functions
def gettext(message):
    # Simple fallback - in real Zid this would use actual translations
    return message

def ngettext(singular, plural, n):
    return singular if n == 1 else plural

# Add global functions
def image_url_func(image_path, w=None, h=None, q=100, f='auto'):
    if not image_path:
        return '/assets/woman.png'  # default image
    if image_path.startswith('/assets'):
        return image_path
    return f'/assets/{image_path.split("/")[-1] if "/" in image_path else image_path}'

def safeget(obj, path, default=None):
    """Safe get function to access nested dictionary keys"""
    try:
        keys = path.split('.')
        for key in keys:
            obj = obj[key]
        return obj
    except (KeyError, TypeError, AttributeError):
        return default

def custom_url_for(endpoint, **kwargs):
    """Custom url_for function for template compatibility"""
    from flask import url_for as flask_url_for
    try:
        # Handle query_params specially
        query_params = kwargs.pop('query_params', {})
        url = flask_url_for(endpoint, **kwargs)
        
        # Add query parameters if provided
        if query_params:
            query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
            url = f"{url}?{query_string}"
        
        return url
    except:
        # Fallback for unknown endpoints
        if endpoint == 'home':
            return '/'
        elif endpoint == 'login_page':
            return '/login'
        elif endpoint == 'list_products':
            return '/products'
        elif endpoint == 'product_questions':
            slug = kwargs.get('slug', 'product')
            return f'/product/{slug}/questions'
        return f'/{endpoint}'

app.jinja_env.globals['_'] = gettext
app.jinja_env.globals['gettext'] = gettext
app.jinja_env.globals['ngettext'] = ngettext
app.jinja_env.globals['image_url'] = image_url_func
app.jinja_env.globals['safeget'] = safeget
app.jinja_env.globals['url_for'] = custom_url_for
app.jinja_env.globals['settings'] = SAMPLE_DATA['settings']
app.jinja_env.globals['store'] = SAMPLE_DATA['store']
app.jinja_env.globals['cart'] = SAMPLE_DATA['cart']
app.jinja_env.globals['products'] = SAMPLE_DATA['products']
app.jinja_env.globals['categories'] = SAMPLE_DATA['categories']
app.jinja_env.globals['currency'] = SAMPLE_DATA['store']['currency']

# Helper class for URL handling
class MockURL:
    def __init__(self, path='/', query_params=None):
        self.path = path
        self.query_params = query_params or {}
    
    def include_query_params(self, **kwargs):
        """Mock function to handle query parameter inclusion"""
        current_params = self.query_params.copy()
        current_params.update(kwargs)
        
        # Build query string
        if current_params:
            query_string = '&'.join([f"{k}={v}" for k, v in current_params.items()])
            return f"{self.path}?{query_string}"
        return self.path

# Add a context processor to inject all data into templates
@app.context_processor
def inject_globals():
    # Get current request path and query parameters
    current_path = request.path
    current_query_params = dict(request.args)
    
    return {
        'session': {
            'locale': MockLocale('ar'),
            'lang': 'ar',
            'language': MockLocale('ar'),
            'currency': {'code': 'SAR', 'symbol': 'ر.س'},
            'template': 'home',
            'is_guest': True,
            'query_params': current_query_params,
            'url': MockURL(current_path, current_query_params),
            'path': current_path
        }
    }

if __name__ == '__main__':
    print("🚀 Starting Zid Theme Development Server...")
    print("📱 Open your browser to: http://localhost:8000")
    print("🔄 Templates will auto-reload on changes")
    print("⏹️  Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=8000)