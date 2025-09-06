from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

class Category(db.Model):
    """Category model for organizing portfolio images"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to portfolio images
    images = db.relationship('PortfolioImage', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'display_order': self.display_order,
            'is_active': self.is_active,
            'image_count': len(self.images),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class PortfolioImage(db.Model):
    """Portfolio image model for managing photography portfolio"""
    __tablename__ = 'portfolio_images'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    alt_text = db.Column(db.String(255))
    
    # Category relationship
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Image metadata
    file_size = db.Column(db.Integer)  # in bytes
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    format = db.Column(db.String(10))  # jpg, png, etc.
    
    # EXIF data (stored as JSON string)
    exif_data = db.Column(db.Text)  # JSON string of EXIF data
    camera_make = db.Column(db.String(100))
    camera_model = db.Column(db.String(100))
    lens = db.Column(db.String(100))
    focal_length = db.Column(db.String(50))
    aperture = db.Column(db.String(50))
    shutter_speed = db.Column(db.String(50))
    iso = db.Column(db.String(50))
    date_taken = db.Column(db.DateTime)
    
    # Portfolio management
    display_order = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PortfolioImage {self.filename}>'
    
    @property
    def file_path(self):
        """Get the full file path for the image"""
        return os.path.join('/data', self.filename)
    
    @property
    def web_path(self):
        """Get the web-accessible path for the image"""
        return f'/data/{self.filename}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'title': self.title,
            'description': self.description,
            'alt_text': self.alt_text,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'file_size': self.file_size,
            'width': self.width,
            'height': self.height,
            'format': self.format,
            'camera_make': self.camera_make,
            'camera_model': self.camera_model,
            'lens': self.lens,
            'focal_length': self.focal_length,
            'aperture': self.aperture,
            'shutter_speed': self.shutter_speed,
            'iso': self.iso,
            'date_taken': self.date_taken.isoformat() if self.date_taken else None,
            'display_order': self.display_order,
            'is_featured': self.is_featured,
            'is_published': self.is_published,
            'web_path': self.web_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class FeaturedImage(db.Model):
    """Model for managing the featured image display"""
    __tablename__ = 'featured_images'
    
    id = db.Column(db.Integer, primary_key=True)
    portfolio_image_id = db.Column(db.Integer, db.ForeignKey('portfolio_images.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to portfolio image
    portfolio_image = db.relationship('PortfolioImage', backref='featured_entries')
    
    def __repr__(self):
        return f'<FeaturedImage {self.portfolio_image.filename if self.portfolio_image else "None"}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'portfolio_image_id': self.portfolio_image_id,
            'is_active': self.is_active,
            'portfolio_image': self.portfolio_image.to_dict() if self.portfolio_image else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

