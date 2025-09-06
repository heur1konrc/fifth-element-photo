import os
import json
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from models.portfolio import db, Category, PortfolioImage, FeaturedImage
from werkzeug.utils import secure_filename

def scan_data_directory():
    """Scan /data directory for image files and return list of image info"""
    data_dir = '/data'
    if not os.path.exists(data_dir):
        return []
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    images = []
    
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, data_dir)
                
                # Get basic file info
                stat = os.stat(file_path)
                file_size = stat.st_size
                created_at = datetime.fromtimestamp(stat.st_ctime)
                
                # Try to get image dimensions and EXIF
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                        exif_data = extract_exif_data(img)
                except Exception as e:
                    width = height = 0
                    exif_data = {}
                
                images.append({
                    'filename': relative_path,
                    'original_filename': file,
                    'file_size': file_size,
                    'width': width,
                    'height': height,
                    'created_at': created_at,
                    'exif_data': exif_data,
                    'web_path': f'/data/{relative_path}'
                })
    
    return images

def extract_exif_data(image):
    """Extract EXIF data from PIL Image object"""
    exif_data = {}
    
    try:
        exif = image._getexif()
        if exif:
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_data[tag] = str(value)
    except Exception:
        pass
    
    return exif_data

def import_images_from_data():
    """Import all images from /data directory into database"""
    images = scan_data_directory()
    imported_count = 0
    skipped_count = 0
    
    # Get default category (first one)
    default_category = Category.query.first()
    
    for img_info in images:
        # Check if image already exists in database
        existing = PortfolioImage.query.filter_by(filename=img_info['filename']).first()
        if existing:
            skipped_count += 1
            continue
        
        # Create new portfolio image
        portfolio_image = PortfolioImage(
            filename=img_info['filename'],
            original_filename=img_info['original_filename'],
            title=os.path.splitext(img_info['original_filename'])[0].replace('_', ' ').replace('-', ' ').title(),
            description='',
            alt_text=f"Photography by Fifth Element Photography",
            file_size=img_info['file_size'],
            width=img_info['width'],
            height=img_info['height'],
            exif_data=json.dumps(img_info['exif_data']),
            web_path=img_info['web_path'],
            category_id=default_category.id if default_category else None,
            is_published=True,
            display_order=0,
            created_at=img_info['created_at']
        )
        
        db.session.add(portfolio_image)
        imported_count += 1
    
    try:
        db.session.commit()
        return {
            'success': True,
            'imported': imported_count,
            'skipped': skipped_count,
            'total_found': len(images)
        }
    except Exception as e:
        db.session.rollback()
        return {
            'success': False,
            'error': str(e),
            'imported': 0,
            'skipped': 0,
            'total_found': len(images)
        }

def get_portfolio_stats():
    """Get portfolio statistics"""
    total_images = PortfolioImage.query.count()
    published_images = PortfolioImage.query.filter_by(is_published=True).count()
    total_categories = Category.query.filter_by(is_active=True).count()
    featured_image = FeaturedImage.query.filter_by(is_active=True).first()
    
    # Get images per category
    category_stats = []
    categories = Category.query.filter_by(is_active=True).all()
    for category in categories:
        image_count = PortfolioImage.query.filter_by(category_id=category.id, is_published=True).count()
        category_stats.append({
            'name': category.name,
            'count': image_count
        })
    
    return {
        'total_images': total_images,
        'published_images': published_images,
        'total_categories': total_categories,
        'has_featured_image': featured_image is not None,
        'category_stats': category_stats
    }

def update_image_category(image_id, category_id):
    """Update image category"""
    try:
        image = PortfolioImage.query.get(image_id)
        if image:
            image.category_id = category_id
            db.session.commit()
            return {'success': True}
        return {'success': False, 'error': 'Image not found'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'error': str(e)}

def update_image_details(image_id, title, description, alt_text, is_published):
    """Update image details"""
    try:
        image = PortfolioImage.query.get(image_id)
        if image:
            image.title = title
            image.description = description
            image.alt_text = alt_text
            image.is_published = is_published
            db.session.commit()
            return {'success': True}
        return {'success': False, 'error': 'Image not found'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'error': str(e)}

def delete_image(image_id):
    """Delete image from database (not from file system)"""
    try:
        image = PortfolioImage.query.get(image_id)
        if image:
            db.session.delete(image)
            db.session.commit()
            return {'success': True}
        return {'success': False, 'error': 'Image not found'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'error': str(e)}

def set_featured_image(image_id):
    """Set an image as the featured image"""
    try:
        # Deactivate current featured image
        current_featured = FeaturedImage.query.filter_by(is_active=True).first()
        if current_featured:
            current_featured.is_active = False
        
        # Set new featured image
        featured = FeaturedImage(
            portfolio_image_id=image_id,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.session.add(featured)
        db.session.commit()
        return {'success': True}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'error': str(e)}

