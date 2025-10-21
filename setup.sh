#!/bin/bash
set -e
# Run as root on Ubuntu 22.04+
PROJECT_DIR=/opt/ecoriego
echo "Creating project dir $PROJECT_DIR"
mkdir -p $PROJECT_DIR
cp -r * $PROJECT_DIR/
cd $PROJECT_DIR/backend
apt update
apt install -y python3-venv python3-pip nginx mysql-server
# create venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# configure mysql - creates db and user
mysql -e "CREATE DATABASE IF NOT EXISTS venue; CREATE USER IF NOT EXISTS 'venue_user'@'localhost' IDENTIFIED BY 'venue_pass'; GRANT ALL PRIVILEGES ON venue.* TO 'venue_user'@'localhost'; FLUSH PRIVILEGES;"
# export env vars for systemd service (alternative: set them in systemd file)
export DATABASE_URL='mysql+pymysql://venue_user:venue_pass@localhost:3306/venue'
export SECRET_KEY='change-me-in-prod'
export JWT_SECRET_KEY='change-me-too'
# initialize DB
python -c "from app.manage_db import *"
# copy frontend to /var/www
mkdir -p /var/www/ecoriego/frontend
cp -r ../frontend/* /var/www/ecoriego/frontend/
# setup systemd service for gunicorn
cat >/etc/systemd/system/ecoriego.service <<EOL
[Unit]
Description=Ecoriego Gunicorn
After=network.target

[Service]
User=root
WorkingDirectory=$PROJECT_DIR/backend
Environment=DATABASE_URL='mysql+pymysql://venue_user:venue_pass@localhost:3306/venue'
Environment=SECRET_KEY='change-me-in-prod'
Environment=JWT_SECRET_KEY='change-me-too'
ExecStart=$PROJECT_DIR/backend/.venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 server:app

[Install]
WantedBy=multi-user.target
EOL
systemctl daemon-reload
systemctl enable --now ecoriego.service
# configure nginx
cp $PROJECT_DIR/nginx_ecoriego.conf /etc/nginx/sites-available/ecoriego.conf
ln -sf /etc/nginx/sites-available/ecoriego.conf /etc/nginx/sites-enabled/ecoriego.conf
nginx -t
systemctl restart nginx
echo "Setup complete. Visit http://your_server_ip or configure DNS to point ecoriego.es to this server."
