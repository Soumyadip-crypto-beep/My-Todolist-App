# 📝 TaskFlow - Modern Todo & YouTube Downloader

A beautiful, modern productivity app built with Flask featuring task management, YouTube video/audio downloading, and PWA capabilities.

## ✨ Features

- **📋 Advanced Task Management**
  - Priority levels (High, Medium, Low)
  - Real-time search and filtering
  - Progress tracking with visual indicators
  - Bulk operations (complete all, delete completed)
  - Task export functionality

- **📺 YouTube Downloader**
  - Download videos in multiple qualities
  - Audio-only downloads
  - Format selection (MP4, WebM, M4A)
  - Video information preview

- **📱 Progressive Web App (PWA)**
  - Installable on mobile devices
  - Offline functionality
  - Native app-like experience
  - QR code installation

- **🎨 Modern UI/UX**
  - Glassmorphism design
  - Responsive mobile-first design
  - Smooth animations and transitions
  - Dark theme optimized

## 🚀 Live Demo

[Visit TaskFlow](https://your-app-name.herokuapp.com)

## 📱 Installation

### Quick Install (Mobile)
1. Visit the app URL on your mobile device
2. Tap "Install App" or use browser's "Add to Home Screen"
3. Enjoy native app experience!

### QR Code Install
Scan the QR code on the install page for instant mobile installation.

## 🛠️ Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/taskflow.git
cd taskflow

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Visit `http://localhost:5000`

## 🌐 Deployment

### Heroku (One-Click Deploy)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Manual Deployment
1. **Render.com** (Recommended)
   - Connect GitHub repository
   - Auto-deploy on push
   - Free tier available

2. **Railway**
   - GitHub integration
   - Automatic deployments
   - Simple configuration

3. **Vercel/Netlify**
   - Static hosting with serverless functions
   - Global CDN
   - Custom domains

## ⚙️ Environment Variables

For production deployment, set these environment variables:

```bash
FLASK_ENV=production
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

## 📦 Dependencies

- **Flask** - Web framework
- **yt-dlp** - YouTube downloader
- **smtplib** - Email functionality

## 🎯 Usage

### Task Management
1. Add tasks with priority levels
2. Use search to find specific tasks
3. Filter by status or priority
4. Track progress with visual indicators
5. Export tasks as JSON

### YouTube Downloader
1. Paste YouTube URL
2. Select desired quality/format
3. Download video or audio
4. Enjoy offline content

### PWA Installation
1. Visit install page
2. Follow platform-specific instructions
3. Install as native app
4. Access from home screen

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**SOUMYADIP JANA**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your-email@gmail.com

## 🙏 Acknowledgments

- Flask community for the amazing framework
- yt-dlp developers for YouTube downloading capabilities
- Modern web standards for PWA functionality

---

Made with ❤️ by SOUMYADIP JANA