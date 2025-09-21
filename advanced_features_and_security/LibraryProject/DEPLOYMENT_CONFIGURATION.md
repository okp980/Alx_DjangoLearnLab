# HTTPS Deployment Configuration Guide

This document provides comprehensive instructions for deploying the Django Library Project with HTTPS support and enhanced security configurations.

## Table of Contents

1. [SSL/TLS Certificate Setup](#ssltls-certificate-setup)
2. [Nginx Configuration](#nginx-configuration)
3. [Apache Configuration](#apache-configuration)
4. [Docker Configuration](#docker-configuration)
5. [Environment Variables](#environment-variables)
6. [Security Checklist](#security-checklist)
7. [Troubleshooting](#troubleshooting)

## SSL/TLS Certificate Setup

### Option 1: Let's Encrypt (Recommended for Production)

```bash
# Install Certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal setup
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

### Option 2: Self-Signed Certificate (Development/Testing)

```bash
# Generate private key
openssl genrsa -out private.key 2048

# Generate certificate signing request
openssl req -new -key private.key -out certificate.csr

# Generate self-signed certificate
openssl x509 -req -days 365 -in certificate.csr -signkey private.key -out certificate.crt
```

## Nginx Configuration

### Basic HTTPS Configuration

Create `/etc/nginx/sites-available/libraryproject`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS Configuration
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    # SSL Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # HSTS Headers (handled by Django)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none';" always;

    # Static files
    location /static/ {
        alias /path/to/your/project/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /path/to/your/project/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
    }
}
```

### Enable the Configuration

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/libraryproject /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

## Apache Configuration

### Virtual Host Configuration

Create `/etc/apache2/sites-available/libraryproject.conf`:

```apache
# Redirect HTTP to HTTPS
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

# HTTPS Configuration
<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    DocumentRoot /path/to/your/project

    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /path/to/certificate.crt
    SSLCertificateKeyFile /path/to/private.key

    # SSL Security Settings
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305
    SSLHonorCipherOrder off
    SSLSessionTickets off

    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"

    # Static files
    Alias /static/ /path/to/your/project/static/
    <Directory /path/to/your/project/static/>
        Require all granted
        ExpiresActive On
        ExpiresDefault "access plus 1 year"
    </Directory>

    # Media files
    Alias /media/ /path/to/your/project/media/
    <Directory /path/to/your/project/media/>
        Require all granted
        ExpiresActive On
        ExpiresDefault "access plus 1 year"
    </Directory>

    # Django application
    WSGIScriptAlias / /path/to/your/project/LibraryProject/wsgi.py
    WSGIDaemonProcess libraryproject python-path=/path/to/your/project python-home=/path/to/venv
    WSGIProcessGroup libraryproject
    WSGIApplicationGroup %{GLOBAL}

    <Directory /path/to/your/project/LibraryProject>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
</VirtualHost>
```

### Enable the Configuration

```bash
# Enable required modules
sudo a2enmod ssl
sudo a2enmod headers
sudo a2enmod rewrite
sudo a2enmod wsgi

# Enable the site
sudo a2ensite libraryproject.conf

# Test configuration
sudo apache2ctl configtest

# Restart Apache
sudo systemctl restart apache2
```

## Docker Configuration

### Dockerfile with HTTPS Support

```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=LibraryProject.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        nginx \
        supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create directories
RUN mkdir -p /app/logs /app/static /app/media

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/sites-available/default
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose ports
EXPOSE 80 443

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

### Docker Compose Configuration

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./static:/app/static
      - ./media:/app/media
      - ./logs:/app/logs
      - ./ssl:/etc/ssl/certs
    environment:
      - DEBUG=False
      - SECRET_KEY=your-secret-key-here
      - DATABASE_URL=postgresql://user:password@db:5432/libraryproject
    depends_on:
      - db

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=libraryproject
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password

volumes:
  postgres_data:
```

## Environment Variables

Create a `.env` file for production:

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/libraryproject

# Security
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True

# Email (for production)
EMAIL_HOST=smtp.yourdomain.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
```

## Security Checklist

### Pre-Deployment Checklist

- [ ] SSL/TLS certificate installed and valid
- [ ] All HTTP traffic redirected to HTTPS
- [ ] Django security settings configured
- [ ] Database credentials secured
- [ ] Secret key is unique and secure
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS configured correctly
- [ ] Static and media files served securely
- [ ] Logging configured for security events
- [ ] Backup strategy implemented

### Post-Deployment Verification

```bash
# Test SSL configuration
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Check security headers
curl -I https://yourdomain.com

# Verify HTTPS redirect
curl -I http://yourdomain.com

# Test HSTS header
curl -I https://yourdomain.com | grep -i strict-transport-security
```

## Troubleshooting

### Common Issues

1. **Mixed Content Warnings**

   - Ensure all resources (CSS, JS, images) are served over HTTPS
   - Update any hardcoded HTTP URLs in templates

2. **CSRF Token Issues**

   - Verify CSRF_TRUSTED_ORIGINS includes your HTTPS domain
   - Check that CSRF_COOKIE_SECURE is True

3. **Session Issues**

   - Ensure SESSION_COOKIE_SECURE is True
   - Verify session cookies are being set correctly

4. **Static Files Not Loading**
   - Check that STATIC_URL and STATIC_ROOT are configured
   - Verify web server is serving static files correctly

### Debug Commands

```bash
# Check Django configuration
python manage.py check --deploy

# Test SSL certificate
openssl x509 -in certificate.crt -text -noout

# Check Nginx configuration
sudo nginx -t

# Check Apache configuration
sudo apache2ctl configtest

# View security logs
tail -f /path/to/logs/django_security.log
```

## Additional Security Recommendations

1. **Regular Security Updates**

   - Keep Django and all dependencies updated
   - Monitor security advisories
   - Implement automated security scanning

2. **Monitoring and Logging**

   - Set up log monitoring for security events
   - Implement intrusion detection
   - Regular security audits

3. **Backup and Recovery**

   - Implement regular database backups
   - Test recovery procedures
   - Store backups securely

4. **Access Control**
   - Use strong authentication
   - Implement rate limiting
   - Regular access reviews

This configuration ensures your Django application is deployed with comprehensive HTTPS support and enhanced security measures.
