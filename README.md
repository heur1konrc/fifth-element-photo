# Fifth Element Photography

**Capturing the Quintessence**

A sophisticated, dark artistic photography portfolio website with creative layouts and mobile-first design.

## Features

- **Artistic Design**: Unique layouts, creative navigation, and artistic flair
- **Mobile-First**: Responsive design optimized for all devices
- **Dynamic Portfolio**: Admin-managed image galleries with category system
- **Creative Navigation**: Animated menus and artistic transitions
- **Admin Management**: Full backend admin tools for content management
- **Contact Integration**: Mailgun-powered contact forms
- **EXIF Display**: Featured images with technical camera data

## Tech Stack

- **Backend**: Flask with SQLAlchemy
- **Frontend**: React with Tailwind CSS
- **Animations**: Framer Motion for artistic effects
- **UI Components**: shadcn/ui for consistent design
- **Database**: SQLite with admin interface
- **Deployment**: Railway

## Project Structure

```
├── backend/          # Flask API and admin tools
│   ├── src/
│   │   ├── models/   # Database models
│   │   ├── routes/   # API endpoints
│   │   └── static/   # Built frontend files
├── frontend/         # React application
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/      # Page components
│   │   └── assets/     # Images and assets
└── README.md
```

## Development

### Backend
```bash
cd backend
source venv/bin/activate
python src/main.py
```

### Frontend
```bash
cd frontend
pnpm run dev
```

## Deployment

The application is designed for Railway deployment with automatic builds from the main branch.

