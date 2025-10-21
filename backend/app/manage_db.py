from app import create_app, db
from app.models import User, Event, RoleEnum
from datetime import datetime
app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(email='admin@ecoriego.es').first():
        u = User(email='admin@ecoriego.es', name='Admin', role=RoleEnum.admin); u.set_password('AdminPass123!'); db.session.add(u)
    if not User.query.filter_by(email='rrpp@ecoriego.es').first():
        r = User(email='rrpp@ecoriego.es', name='RRPP', role=RoleEnum.rrpp); r.set_password('RrppPass123!'); db.session.add(r)
    if not User.query.filter_by(email='scanner@ecoriego.es').first():
        s = User(email='scanner@ecoriego.es', name='Scanner', role=RoleEnum.scanner); s.set_password('ScanPass123!'); db.session.add(s)
    if not Event.query.first():
        ev = Event(title='Noche Indie - Gijón', date=datetime.fromisoformat('2025-10-25T22:00:00'), capacity=500, zones={'pista':400,'vip':100}); db.session.add(ev)
    db.session.commit()
    print('seeded')
