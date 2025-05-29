# 📰 TechPulse - Modern Django Blog Platform with M-Pesa Integration

<div align="center">
  <img src="https://github.com/user-attachments/assets/cda40bc8-0e2a-4f05-bdc8-d5a7de52f042" alt="TechPulse Homepage" width="800"/>
  
  <p><em>A feature-rich, mobile-responsive blog platform built with Django & Bootstrap, enhanced with M-Pesa payment integration for subscription-based content access.</em></p>
  
  [![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://www.djangoproject.com/)
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
  [![M-Pesa](https://img.shields.io/badge/M--Pesa-STK%20Push-success.svg)](https://developer.safaricom.co.ke/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

---

> ✅ **Project developed during industrial attachment at [Masyopnet Technologies](https://masyopnet.co.ke)**  
> 🎓 **Continuation of previous RESTful API project – now featuring full frontend integration, M-Pesa payments, and advanced admin controls**  
> 🌟 **Special appreciation to Masyopnet Technologies for providing the learning environment and mentorship**

---

## 🚀 Project Overview

TechPulse is a modern, full-stack blog platform that demonstrates the integration of Django backend development with real-world payment processing. Built as an extension of my previous API project, this platform showcases advanced web development skills including payment gateway integration, responsive UI design, and comprehensive content management.

### 🎯 Key Achievements

- **Full-Stack Development**: Seamless integration of Django backend with responsive Bootstrap frontend
- **Payment Integration**: Successfully implemented M-Pesa STK Push for subscription management
- **Real-World Application**: Production-ready platform with comprehensive testing and deployment strategies
- **API Development**: RESTful API with JWT authentication for mobile/web client integration
- **Modern UI/UX**: Mobile-first design with professional user experience

## 📌 Core Features

### 🔥 Blog Platform Features
* ✅ **Responsive Design** - Bootstrap 5 with mobile-first approach
* ✅ **User Management** - Registration, authentication, and profile management
* ✅ **Content Creation** - Rich text editor for creating and editing blog posts
* ✅ **Organization** - Categories, tags, and advanced filtering systems
* ✅ **Engagement** - Nested comments with threaded replies
* ✅ **Search** - Real-time search functionality across all content
* ✅ **Admin Dashboard** - Comprehensive content and user management

### 💰 M-Pesa Payment Integration
* ✔️ **STK Push Gateway** - Direct mobile payment integration via Safaricom Daraja API
* ✔️ **Subscription Plans** - Flexible Basic (KSh 150) and Premium (KSh 250) tiers
* ✔️ **Real-time Processing** - Instant payment confirmation and status updates
* ✔️ **Secure Transactions** - Industry-standard security with callback verification
* ✔️ **Sandbox Testing** - Complete testing environment for development

### 📊 Advanced Features
* 🔐 **JWT Authentication** - Secure API access for mobile applications
* 📱 **Mobile Responsive** - Optimized for all device sizes
* 🎨 **Modern UI** - Clean, professional design with smooth animations
* 📧 **Email Integration** - Password reset and notification system
* 🔍 **SEO Optimized** - Search engine friendly URLs and meta tags

---

## 📸 Application Screenshots

### Homepage & Navigation
![TechPulse Homepage](https://github.com/user-attachments/assets/cda40bc8-0e2a-4f05-bdc8-d5a7de52f042)
*Modern homepage with featured articles, breaking news ticker, and intuitive navigation*

### Article Management
![Articles View](https://github.com/user-attachments/assets/31e8d740-5c19-4035-93b8-21c072c9c470)
*Clean article layout with category filtering and responsive card design*

### Subscription System
![Subscription Plans](https://github.com/user-attachments/assets/93664583-9372-4965-9e5e-d2b4857e3ee7)
*Professional subscription plans with integrated M-Pesa payment options*

### M-Pesa Integration
![M-Pesa STK Push](https://github.com/user-attachments/assets/72e12732-ece8-4664-84fe-c4dd0db8cbd7)
*Real M-Pesa STK Push notification demonstrating successful payment integration*

---

## 🛠️ Technology Stack

### Backend Technologies
- **Django 4.2.7** - Robust web framework with ORM
- **Django REST Framework** - API development and serialization
- **SQLite/PostgreSQL** - Database management (production-ready)
- **JWT Authentication** - Secure token-based authentication
- **Python Decouple** - Environment configuration management

### Frontend Technologies
- **Bootstrap 5** - Responsive CSS framework
- **JavaScript (ES6+)** - Modern client-side functionality
- **Font Awesome** - Professional icon library
- **Google Fonts (Inter)** - Modern typography
- **Custom CSS** - Enhanced styling and animations

### Payment Integration
- **Safaricom Daraja API** - M-Pesa payment gateway
- **STK Push** - Mobile payment processing
- **Webhook Handling** - Real-time payment confirmations
- **Sandbox Testing** - Development and testing environment

### Development Tools
- **Django Crispy Forms** - Enhanced form rendering
- **Django CORS Headers** - Cross-origin resource sharing
- **Requests Library** - HTTP client for API calls
- **Logging Framework** - Comprehensive error tracking

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)
- M-Pesa Developer Account (for payment features)

### Step 1: Repository Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/techpulse-blog.git
cd techpulse-blog

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\\Scripts\\activate  # Windows
```

### Step 2: Dependencies Installation
```bash
# Install required packages
pip install -r requirements.txt

# Install additional dependencies for M-Pesa
pip install requests python-decouple
```

### Step 3: Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configurations
nano .env
```

### Step 4: Environment Variables
Create a `.env` file with the following configurations:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database Configuration (Optional - defaults to SQLite)
DATABASE_URL=postgresql://username:password@localhost:5432/techpulse_db

# M-Pesa Configuration (Safaricom Daraja API)
DARAJA_ENVIRONMENT=sandbox  # Use 'production' for live environment
DARAJA_CONSUMER_KEY=your-consumer-key-from-safaricom
DARAJA_CONSUMER_SECRET=your-consumer-secret-from-safaricom
DARAJA_SHORTCODE=your-business-shortcode
DARAJA_PASSKEY=your-lipa-na-mpesa-passkey
DARAJA_CALLBACK_URL=https://yourdomain.com/api/mpesa/callback/

# Email Configuration (for password reset)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security Settings (Production)
SECURE_SSL_REDIRECT=False
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

### Step 5: Database Setup
```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser

# Load sample data (optional)
python manage.py populate_sample_data
```

### Step 6: Run Development Server
```bash
# Start the development server
python manage.py runserver

# Access the application
# Homepage: http://127.0.0.1:8000/
# Admin: http://127.0.0.1:8000/admin/
# API: http://127.0.0.1:8000/api/
```

---

## 🔧 M-Pesa Integration Setup

### Safaricom Developer Portal Setup

1. **Create Developer Account**
   - Visit [developer.safaricom.co.ke](https://developer.safaricom.co.ke)
   - Register for a new account
   - Verify your email and complete profile

2. **Create New Application**
   - Navigate to "My Apps" section
   - Click "Create New App"
   - Select "Lipa Na M-Pesa Sandbox" for testing
   - Note down Consumer Key and Consumer Secret

3. **Configure STK Push**
   - Set up business shortcode and passkey
   - Configure callback URL for payment notifications
   - Test credentials in sandbox environment

### Testing M-Pesa Integration

```bash
# Test M-Pesa connectivity
python manage.py test_mpesa --phone=254708374149 --amount=1

# Debug M-Pesa setup
./debug_mpesa_complete.sh

# Run comprehensive tests
python manage.py test blog.tests.test_mpesa
```

### Sandbox Test Numbers
- **Test Phone**: 254708374149 (won't receive actual STK push)
- **Test Amount**: Any amount (KSh 1-50,000 for sandbox)
- **Expected Response**: Success confirmation without real money transfer

---

## 📡 API Documentation

### Authentication Endpoints
```http
POST /api/token/                    # Obtain JWT access token
POST /api/token/refresh/            # Refresh JWT token
```

### Blog Content API
```http
GET    /api/posts/                  # List all published posts
POST   /api/posts/                  # Create new post (authenticated)
GET    /api/posts/{slug}/           # Get specific post details
PUT    /api/posts/{slug}/           # Update post (author only)
DELETE /api/posts/{slug}/           # Delete post (author only)
```

### Comments API
```http
GET  /api/posts/{slug}/comments/    # List post comments
POST /api/posts/{slug}/comments/    # Add new comment (authenticated)
```

### User Management API
```http
GET /api/user/posts/                # List user's posts
GET /api/user/profile/              # Get user profile
PUT /api/user/profile/              # Update user profile
```

### Categories & Tags API
```http
GET /api/categories/                # List all categories
GET /api/tags/                      # List all tags
```

### Statistics API
```http
GET /api/stats/                     # Get blog statistics
GET /api/popular-posts/             # Get most popular posts
GET /api/recent-posts/              # Get recent posts
```

### API Usage Example
```javascript
// Obtain JWT token
const response = await fetch('/api/token/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'your_username',
        password: 'your_password'
    })
});

const data = await response.json();
const token = data.access;

// Use token for authenticated requests
const postsResponse = await fetch('/api/posts/', {
    headers: {
        'Authorization': `Bearer \${token}`
    }
});
```

---

## 🧪 Testing

### Running Test Suite
```bash
# Run all tests
python manage.py test

# Run specific test modules
python manage.py test blog.tests.test_models
python manage.py test blog.tests.test_views
python manage.py test blog.tests.test_mpesa

# Run tests with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### M-Pesa Testing Tools
```bash
# Quick M-Pesa test
python manage.py test_mpesa

# Comprehensive M-Pesa debug
./debug_mpesa_complete.sh

# Test with custom parameters
python manage.py test_mpesa --phone=254712345678 --amount=50
```

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Post creation and editing
- [ ] Comment system functionality
- [ ] Search and filtering
- [ ] M-Pesa payment flow
- [ ] Admin dashboard access
- [ ] API endpoints
- [ ] Mobile responsiveness

---

## 🚀 Deployment

### Production Deployment Checklist

#### Security Configuration
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS and SSL
- [ ] Set secure headers

#### Database Setup
- [ ] Configure PostgreSQL for production
- [ ] Run database migrations
- [ ] Set up database backups
- [ ] Configure connection pooling

#### Static Files
- [ ] Configure static file serving
- [ ] Use WhiteNoise or CDN
- [ ] Compress and optimize assets
- [ ] Set proper cache headers

#### M-Pesa Production
- [ ] Switch to production environment
- [ ] Update callback URLs
- [ ] Test with real transactions
- [ ] Monitor payment logs

### Recommended Deployment Platforms

#### **Railway** (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

#### **Heroku**
```bash
# Create Heroku app
heroku create techpulse-blog

# Configure environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main
```

#### **DigitalOcean App Platform**
- Connect GitHub repository
- Configure environment variables
- Set build and run commands
- Deploy with automatic scaling

---

## 🎨 Customization Guide

### Theming and Styling
```css
/* Custom CSS variables in static/css/style.css */
:root {
    --primary-color: #0a84ff;
    --secondary-color: #64748b;
    --success-color: #10b981;
    --background: #ffffff;
    --text-primary: #1e293b;
}
```

### Adding New Features
1. **Create new Django app**: `python manage.py startapp newfeature`
2. **Add to INSTALLED_APPS** in settings.py
3. **Create models, views, and templates**
4. **Add URL patterns**
5. **Create API endpoints** if needed

### Extending the API
```python
# Example: Add new API endpoint in api/views.py
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def custom_endpoint(request):
    data = {'message': 'Custom endpoint'}
    return Response(data)
```

---

## 📊 Performance Optimization

### Database Optimization
- Use `select_related()` and `prefetch_related()` for efficient queries
- Add database indexes for frequently queried fields
- Implement database connection pooling
- Use database query optimization tools

### Caching Strategy
```python
# Add caching to views
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def home_view(request):
    # View logic here
    pass
```

### Frontend Optimization
- Compress CSS and JavaScript files
- Optimize images and use appropriate formats
- Implement lazy loading for images
- Use CDN for static assets

---

## 🔒 Security Considerations

### Django Security Best Practices
- Keep Django and dependencies updated
- Use HTTPS in production
- Implement proper CSRF protection
- Validate and sanitize user inputs
- Use Django's built-in security features

### M-Pesa Security
- Validate callback requests
- Use HTTPS for callback URLs
- Implement request signing verification
- Monitor for suspicious transactions
- Keep API credentials secure

---

## 📝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for changes
- Use meaningful commit messages
- Test M-Pesa integration in sandbox mode

### Reporting Issues
- Use GitHub Issues for bug reports
- Provide detailed reproduction steps
- Include environment information
- Attach relevant log files

---

## 🤝 Credits & Acknowledgments

### Special Recognition
> 🌟 **Heartfelt appreciation to [Masyopnet Technologies](https://masyopnet.co.ke)** for providing the industrial attachment opportunity, mentorship, and supportive learning environment that made this project possible. The hands-on experience and guidance received during my attachment were instrumental in developing both technical skills and professional understanding of real-world software development.

### Technology Partners
- **Safaricom** - For the comprehensive Daraja API and M-Pesa integration platform
- **Django Software Foundation** - For the robust web framework
- **Bootstrap Team** - For the responsive CSS framework
- **Font Awesome** - For the professional icon library
- **Python Software Foundation** - For the programming language

### Development Community
- Django REST Framework contributors
- Open source package maintainers
- Stack Overflow community
- GitHub community

### Professional Development
- **Masyopnet Technologies Team** - For mentorship and code reviews
- **Industry Mentors** - For guidance on best practices
- **Peer Developers** - For collaboration and knowledge sharing

---

## 📞 Support & Contact

### Technical Support

- **Email**: [jacobmuema02@gmail.com](mailto:jacobmuema02@gmail.com)
- **Documentation**: Comprehensive code comments and this README

### M-Pesa Integration Support
- **Safaricom Developer Portal**: [developer.safaricom.co.ke](https://developer.safaricom.co.ke)
- **API Documentation**: [Daraja API Docs](https://developer.safaricom.co.ke/docs)
- **Community Forum**: Safaricom Developer Community

### Professional Inquiries
- **LinkedIn**: [Connect for professional networking](https://www.linkedin.com/in/jacob-muema-256310270/overlay/about-this-profile/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base%3BZfiKPPcJSySk%2FDSVTdAkQg%3D%3D)
- **Portfolio**: [View other projects and achievements](https://kavengijm-featuringmomalways.netlify.app/)


---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### License Summary
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ❗ License and copyright notice required

---

## 🚀 Future Enhancements

### Planned Features
- [ ] **Mobile Application**: React Native app using the REST API
- [ ] **Analytics Dashboard**: Detailed usage and revenue analytics
- [ ] **Email Marketing**: Newsletter system with automated campaigns
- [ ] **SEO Optimization**: Advanced SEO tools and meta tag management
- [ ] **Social Media Integration**: Automatic sharing and social login
- [ ] **Multi-language Support**: Internationalization and localization

### Technical Improvements
- [ ] **Microservices Architecture**: Split into smaller, manageable services
- [ ] **Redis Caching**: Advanced caching for improved performance
- [ ] **Elasticsearch**: Enhanced search functionality
- [ ] **Docker Deployment**: Containerization for easier deployment
- [ ] **CI/CD Pipeline**: Automated testing and deployment
- [ ] **Monitoring**: Application performance monitoring and logging

---

<div align="center">
  
  ### 🏆 Project Achievement Summary
  
  **✅ Full-Stack Development** | **✅ Payment Integration** | **✅ API Development** | **✅ Production Deployment**
  
  ---
  
  <h3>🎓 TechPulse Blog Platform</h3>
  <p><strong>Developed at Masyopnet Technologies</strong></p>
  <p>💻 Built with Django & Bootstrap | 💚 Powered by M-Pesa | 🇰🇪 Made in Kenya</p>
  
  ⭐ **Star this repository if you found it helpful!** ⭐
  
  ---
  
  <p><em>This project represents the culmination of industrial attachment learning, demonstrating practical application of modern web development technologies with real-world payment integration.</em></p>
  
</div>
```

