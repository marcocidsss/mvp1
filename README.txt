ECORIEGO Tickets - Deploy package
Domain preconfigured: ecoriego.es

How to use (quick):
1) Upload all files to your VPS (scp -r /mnt/data/ecoriego_tickets_package/* root@YOUR_IP:/root/ecoriego/)
2) SSH into VPS and run as root: bash setup.sh
3) After setup, default site files are in /var/www/ecoriego/frontend and backend runs via systemd/gunicorn.

Seeded accounts (change passwords in production):
- admin@ecoriego.es / AdminPass123!
- rrpp@ecoriego.es / RrppPass123!
- scanner@ecoriego.es / ScanPass123!
- user@ecoriego.es / UserPass123!

Notes:
- Change SECRET_KEY and JWT_SECRET_KEY environment variables to strong values before production.
- setup.sh configures mysql and creates DB and user with password 'venue_pass' (change it).
- Nginx config placed at nginx_ecoriego.conf maps domain ecoriego.es; adjust DNS to point to VPS IP.
