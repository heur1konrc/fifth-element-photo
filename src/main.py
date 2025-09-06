import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PIL import Image
from PIL.ExifTags import TAGS
import json
from datetime import datetime

# Import models
from src.models.portfolio import db, Category, PortfolioImage, FeaturedImage

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Database configuration
database_dir = os.path.join(os.path.dirname(__file__), 'database')
os.makedirs(database_dir, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(database_dir, 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)
CORS(app)

# Create tables and default data
with app.app_context():
    db.create_all()
    
    # Create default categories if none exist
    if Category.query.count() == 0:
        default_categories = [
            {'name': 'Portraits', 'slug': 'portraits', 'description': 'Portrait photography', 'display_order': 1},
            {'name': 'Landscapes', 'slug': 'landscapes', 'description': 'Landscape photography', 'display_order': 2},
            {'name': 'Street', 'slug': 'street', 'description': 'Street photography', 'display_order': 3},
            {'name': 'Events', 'slug': 'events', 'description': 'Event photography', 'display_order': 4},
            {'name': 'Commercial', 'slug': 'commercial', 'description': 'Commercial photography', 'display_order': 5}
        ]
        
        for cat_data in default_categories:
            category = Category(**cat_data)
            db.session.add(category)
        
        db.session.commit()
        print("Default categories created")

# Data volume routes
@app.route('/data/<path:filename>')
def serve_data_file(filename):
    """Serve files from the /data volume"""
    return send_from_directory('/data', filename)

# API Routes for Portfolio
@app.route('/api/categories')
def get_categories():
    """Get all active categories"""
    categories = Category.query.filter_by(is_active=True).order_by(Category.display_order).all()
    return jsonify([cat.to_dict() for cat in categories])

@app.route('/api/portfolio')
def get_portfolio():
    """Get portfolio images with optional category filtering"""
    category_id = request.args.get('category_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    
    query = PortfolioImage.query.filter_by(is_published=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    query = query.order_by(PortfolioImage.display_order, PortfolioImage.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'images': [img.to_dict() for img in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })

@app.route('/api/featured-image')
def get_featured_image():
    """Get the current featured image"""
    featured = FeaturedImage.query.filter_by(is_active=True).first()
    if featured and featured.portfolio_image:
        return jsonify(featured.portfolio_image.to_dict())
    return jsonify({'error': 'No featured image set'}), 404

# Admin Routes
@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    total_images = PortfolioImage.query.count()
    total_categories = Category.query.filter_by(is_active=True).count()
    featured_image = FeaturedImage.query.filter_by(is_active=True).first()
    
    stats = {
        'total_images': total_images,
        'total_categories': total_categories,
        'has_featured_image': featured_image is not None
    }
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fifth Element Photography - Admin</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: white; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            .header {{ text-align: center; margin-bottom: 40px; }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px; }}
            .stat-card {{ background: #2a2a2a; padding: 20px; border-radius: 8px; text-align: center; }}
            .stat-number {{ font-size: 2em; font-weight: bold; color: #4CAF50; }}
            .nav-links {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }}
            .nav-link {{ background: #333; padding: 20px; border-radius: 8px; text-decoration: none; color: white; text-align: center; transition: background 0.3s; }}
            .nav-link:hover {{ background: #444; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Fifth Element Photography</h1>
                <h2>Admin Dashboard</h2>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{stats['total_images']}</div>
                    <div>Total Images</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats['total_categories']}</div>
                    <div>Categories</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{'✓' if stats['has_featured_image'] else '✗'}</div>
                    <div>Featured Image</div>
                </div>
            </div>
            
            <div class="nav-links">
                <a href="/admin/portfolio" class="nav-link">
                    <h3>Portfolio Management</h3>
                    <p>Upload, organize, and manage your photography portfolio</p>
                </a>
                <a href="/admin/categories" class="nav-link">
                    <h3>Category Management</h3>
                    <p>Create and organize portfolio categories</p>
                </a>
                <a href="/admin/featured" class="nav-link">
                    <h3>Featured Image</h3>
                    <p>Set the featured image with EXIF data display</p>
                </a>
                <a href="/" class="nav-link">
                    <h3>View Website</h3>
                    <p>See your live photography website</p>
                </a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/admin/portfolio')
def admin_portfolio():
    """Portfolio management interface"""
    categories = Category.query.order_by(Category.display_order).all()
    images = PortfolioImage.query.order_by(PortfolioImage.display_order, PortfolioImage.created_at.desc()).all()
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Portfolio Management - Fifth Element Photography</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: white; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
            .btn {{ background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; }}
            .btn:hover {{ background: #45a049; }}
            .portfolio-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }}
            .image-card {{ background: #2a2a2a; border-radius: 8px; overflow: hidden; }}
            .image-card img {{ width: 100%; height: 150px; object-fit: cover; }}
            .image-info {{ padding: 15px; }}
            .category-badge {{ background: #666; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Portfolio Management</h1>
                <div>
                    <a href="/admin" class="btn">← Back to Dashboard</a>
                    <a href="#" class="btn">+ Upload Images</a>
                </div>
            </div>
            
            <div class="portfolio-grid">
                {''.join([f'''
                <div class="image-card">
                    <img src="/data/{img.filename}" alt="{img.title or img.filename}">
                    <div class="image-info">
                        <h4>{img.title or img.filename}</h4>
                        <span class="category-badge">{img.category.name if img.category else 'No Category'}</span>
                        <p>{img.description or 'No description'}</p>
                    </div>
                </div>
                ''' for img in images])}
            </div>
            
            {f'<p style="text-align: center; margin-top: 40px; color: #666;">No images uploaded yet. Start by uploading your first image!</p>' if not images else ''}
        </div>
    </body>
    </html>
    """

@app.route('/admin/categories')
def admin_categories():
    """Category management interface"""
    categories = Category.query.order_by(Category.display_order).all()
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Category Management - Fifth Element Photography</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: white; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
            .btn {{ background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; }}
            .btn:hover {{ background: #45a049; }}
            .category-list {{ background: #2a2a2a; border-radius: 8px; overflow: hidden; }}
            .category-item {{ padding: 20px; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center; }}
            .category-item:last-child {{ border-bottom: none; }}
            .category-info h3 {{ margin: 0 0 5px 0; }}
            .category-info p {{ margin: 0; color: #ccc; }}
            .image-count {{ background: #666; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Category Management</h1>
                <div>
                    <a href="/admin" class="btn">← Back to Dashboard</a>
                    <a href="#" class="btn">+ Add Category</a>
                </div>
            </div>
            
            <div class="category-list">
                {''.join([f'''
                <div class="category-item">
                    <div class="category-info">
                        <h3>{cat.name}</h3>
                        <p>{cat.description or 'No description'}</p>
                    </div>
                    <div class="image-count">{len(cat.images)} images</div>
                </div>
                ''' for cat in categories])}
            </div>
        </div>
    </body>
    </html>
    """

# Frontend routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

