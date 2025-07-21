 # 🚀 Deployment Guide

Panduan lengkap untuk deploy Proyek Pajak Backend ke berbagai platform.

## 📋 Daftar Isi

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Local Development](#local-development)
- [Heroku Deployment](#heroku-deployment)
- [Railway Deployment](#railway-deployment)
- [Vercel Deployment](#vercel-deployment)
- [Docker Deployment](#docker-deployment)
- [AWS EC2 Deployment](#aws-ec2-deployment)
- [Production Considerations](#production-considerations)

## 🔧 Prerequisites

### System Requirements

- Python 3.8+
- PostgreSQL database (Supabase recommended)
- Git
- Node.js (untuk beberapa platform)

### Tools yang Dibutuhkan

- Heroku CLI (untuk Heroku deployment)
- Docker (untuk containerization)
- AWS CLI (untuk AWS deployment)

## 🌱 Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/Taufiqu/proyek-pajak-backend-clean.git
cd proyek-pajak-backend-clean
```

### 2. Environment Variables

Buat file `.env` berdasarkan `.env.example`:

```bash
cp .env.example .env
```

Update variabel environment:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Application
FLASK_PORT=5001
FLASK_ENV=production
FLASK_DEBUG=0

# OCR
POPPLER_PATH=/usr/bin  # Linux
# POPPLER_PATH=C:\\poppler\\poppler-24.08.0\\Library\\bin  # Windows
```

## 🖥️ Local Development

### 1. Setup Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 4. Run Application

```bash
python app.py
```

Server akan berjalan di `http://localhost:5001`

## 🚀 Heroku Deployment

### 1. Install Heroku CLI

```bash
# Windows (chocolatey)
choco install heroku-cli

# macOS
brew install heroku/brew/heroku

# Linux
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
```

### 2. Login ke Heroku

```bash
heroku login
```

### 3. Create Heroku App

```bash
heroku create your-app-name
```

### 4. Add Buildpacks

```bash
heroku buildpacks:add --index 1 heroku-community/apt
heroku buildpacks:add --index 2 heroku/python
```

### 5. Create Aptfile

Buat file `Aptfile` untuk install poppler:

```bash
poppler-utils
```

### 6. Configure Environment Variables

```bash
heroku config:set DATABASE_URL=your-database-url
heroku config:set SUPABASE_URL=your-supabase-url
heroku config:set SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
heroku config:set FLASK_ENV=production
heroku config:set FLASK_DEBUG=0
heroku config:set POPPLER_PATH=/usr/bin
```

### 7. Deploy to Heroku

```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 8. Run Database Migrations

```bash
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 9. Open Application

```bash
heroku open
```

## 🚄 Railway Deployment

### 1. Install Railway CLI

```bash
npm install -g @railway/cli
```

### 2. Login ke Railway

```bash
railway login
```

### 3. Initialize Project

```bash
railway init
```

### 4. Configure Environment Variables

Di Railway dashboard, tambahkan:
- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `FLASK_ENV=production`
- `POPPLER_PATH=/usr/bin`

### 5. Deploy

```bash
railway up
```

## ⚡ Vercel Deployment

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Create vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

### 3. Deploy

```bash
vercel --prod
```

**Note:** Vercel memiliki limitasi untuk file processing yang besar. Pertimbangkan platform lain untuk production.

## 🐳 Docker Deployment

### 1. Build Docker Image

```bash
docker build -t proyek-pajak-backend .
```

### 2. Run Container

```bash
docker run -p 5001:5001 \
  -e DATABASE_URL=your-database-url \
  -e SUPABASE_URL=your-supabase-url \
  -e SUPABASE_SERVICE_ROLE_KEY=your-service-role-key \
  -e FLASK_ENV=production \
  -e POPPLER_PATH=/usr/bin \
  proyek-pajak-backend
```

### 3. Docker Compose

Buat file `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5001:5001"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_SERVICE_ROLE_KEY=${SUPABASE_SERVICE_ROLE_KEY}
      - FLASK_ENV=production
      - POPPLER_PATH=/usr/bin
    env_file:
      - .env
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped
```

Run dengan:

```bash
docker-compose up -d
```

## ☁️ AWS EC2 Deployment

### 1. Launch EC2 Instance

- AMI: Ubuntu 22.04 LTS
- Instance Type: t3.medium (minimum)
- Security Group: Allow HTTP (80), HTTPS (443), SSH (22)

### 2. Connect to Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### 3. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv git nginx

# Install poppler
sudo apt install -y poppler-utils

# Install supervisor for process management
sudo apt install -y supervisor
```

### 4. Setup Application

```bash
# Clone repository
git clone https://github.com/Taufiqu/proyek-pajak-backend-clean.git
cd proyek-pajak-backend-clean

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your values
```

### 5. Configure Gunicorn

Install Gunicorn:

```bash
pip install gunicorn
```

Create `gunicorn.conf.py`:

```python
bind = "127.0.0.1:5001"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
keepalive = 2
user = "ubuntu"
group = "ubuntu"
```

### 6. Configure Supervisor

Create `/etc/supervisor/conf.d/proyek-pajak.conf`:

```ini
[program:proyek-pajak]
command=/home/ubuntu/proyek-pajak-backend-clean/venv/bin/gunicorn -c gunicorn.conf.py app:app
directory=/home/ubuntu/proyek-pajak-backend-clean
user=ubuntu
group=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/proyek-pajak.log
```

### 7. Configure Nginx

Create `/etc/nginx/sites-available/proyek-pajak`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    client_max_body_size 16M;
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }
    
    location /static {
        alias /home/ubuntu/proyek-pajak-backend-clean/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 8. Enable and Start Services

```bash
# Enable nginx site
sudo ln -s /etc/nginx/sites-available/proyek-pajak /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Start supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start proyek-pajak

# Check status
sudo supervisorctl status proyek-pajak
```

### 9. SSL Configuration (Optional)

Install Certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 🔒 Production Considerations

### 1. Security

```bash
# Environment variables
export FLASK_ENV=production
export FLASK_DEBUG=0

# Database security
# - Use connection pooling
# - Enable SSL
# - Regular backups

# File uploads
# - Validate file types
# - Scan for malware
# - Limit file sizes
```

### 2. Performance

```bash
# Caching
# - Redis for session storage
# - CDN for static files
# - Database query optimization

# Monitoring
# - Application logs
# - Error tracking (Sentry)
# - Performance monitoring (New Relic)
```

### 3. Scaling

```bash
# Horizontal scaling
# - Load balancer
# - Multiple app instances
# - Database read replicas

# Vertical scaling
# - Increase server resources
# - Optimize database queries
# - Background job processing
```

### 4. Backup Strategy

```bash
# Database backups
# - Daily automated backups
# - Point-in-time recovery
# - Cross-region replication

# File backups
# - Uploaded files to S3
# - Configuration files
# - Application logs
```

### 5. Monitoring Setup

```bash
# Application monitoring
# - Health checks
# - Performance metrics
# - Error tracking
# - Log aggregation

# Infrastructure monitoring
# - Server resources
# - Database performance
# - Network connectivity
```

### 6. CI/CD Pipeline

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@example.com"
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Check what's using the port
sudo netstat -tulpn | grep :5001

# Kill process
sudo kill -9 PID
```

#### 2. Database Connection Issues

```bash
# Test database connection
python -c "
import os
from sqlalchemy import create_engine
engine = create_engine(os.environ['DATABASE_URL'])
print('Database connection successful')
"
```

#### 3. File Upload Issues

```bash
# Check file permissions
ls -la uploads/
chmod 755 uploads/

# Check disk space
df -h
```

#### 4. OCR Not Working

```bash
# Check poppler installation
which pdftotext
poppler-utils --version

# Test OCR
python -c "
from bukti_setor.utils.ocr_engine import OCREngine
ocr = OCREngine()
print('OCR engine ready')
"
```

### Log Files

```bash
# Application logs
tail -f /var/log/supervisor/proyek-pajak.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# System logs
journalctl -u nginx -f
```

## 📊 Performance Optimization

### 1. Database Optimization

```sql
-- Add indexes
CREATE INDEX idx_ppn_masukan_no_faktur ON ppn_masukan(no_faktur);
CREATE INDEX idx_ppn_masukan_tanggal ON ppn_masukan(tanggal);
CREATE INDEX idx_ppn_keluaran_no_faktur ON ppn_keluaran(no_faktur);
CREATE INDEX idx_ppn_keluaran_tanggal ON ppn_keluaran(tanggal);
CREATE INDEX idx_bukti_setor_tanggal ON bukti_setor(tanggal);
```

### 2. Application Optimization

```python
# config.py
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 20,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
    'max_overflow': 30
}
```

### 3. Caching

```python
# Install redis
pip install redis flask-caching

# config.py
CACHE_TYPE = 'redis'
CACHE_REDIS_URL = 'redis://localhost:6379'
```

---

**🎯 Deployment berhasil!** Aplikasi Anda sekarang siap untuk production. Jangan lupa untuk monitoring dan maintenance secara rutin.
  n