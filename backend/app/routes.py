from flask import Blueprint, request, jsonify, current_app, send_from_directory
from . import db
from .models import User, Event, Ticket, RoleEnum
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return send_from_directory(current_app.static_folder, 'index.html')

@bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email'); name = data.get('name',''); password = data.get('password')
    if not email or not password: return jsonify({'status':'error','message':'missing'}),400
    if User.query.filter_by(email=email).first(): return jsonify({'status':'error','message':'exists'}),400
    u = User(email=email, name=name)
    u.set_password(password)
    db.session.add(u); db.session.commit()
    return jsonify({'status':'ok','user':{'id':u.id,'email':u.email}})

@bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email'); password = data.get('password')
    u = User.query.filter_by(email=email).first()
    if not u or not u.check_password(password): return jsonify({'status':'error','message':'invalid'}),401
    token = create_access_token(identity={'id':u.id,'role':u.role.value,'email':u.email})
    return jsonify({'status':'ok','token':token,'user':{'id':u.id,'email':u.email,'role':u.role.value,'name':u.name}})

@bp.route('/api/events', methods=['GET'])
def list_events():
    evs = Event.query.all()
    out = [{'id':e.id,'title':e.title,'date':e.date.isoformat(),'capacity':e.capacity,'zones':e.zones} for e in evs]
    return jsonify({'status':'ok','events':out})

@bp.route('/api/events', methods=['POST'])
@jwt_required()
def create_event():
    idt = get_jwt_identity()
    if idt.get('role')!='admin': return jsonify({'status':'error','message':'forbidden'}),403
    data = request.get_json() or {}
    ev = Event(title=data.get('title'), date=datetime.fromisoformat(data.get('date')), capacity=int(data.get('capacity',0)), zones=data.get('zones',{}))
    db.session.add(ev); db.session.commit()
    return jsonify({'status':'ok','event':{'id':ev.id,'title':ev.title}})

@bp.route('/api/buy', methods=['POST'])
@jwt_required()
def buy():
    data = request.get_json() or {}
    ev = Event.query.filter_by(id=data.get('event_id')).first()
    if not ev: return jsonify({'status':'error','message':'noevent'}),404
    zone = data.get('zone'); name = data.get('buyer_name'); email = data.get('buyer_email')
    sold = Ticket.query.filter_by(event_id=ev.id, zone=zone).count()
    cap = ev.zones.get(zone,0)
    if sold >= cap: return jsonify({'status':'error','message':'soldout'}),400
    t = Ticket(event_id=ev.id, zone=zone, owner_name=name, owner_email=email, nominative=True)
    db.session.add(t); db.session.commit()
    return jsonify({'status':'ok','ticket':{'id':t.id,'zone':t.zone}})

@bp.route('/api/mytickets', methods=['GET'])
@jwt_required()
def mytickets():
    idt = get_jwt_identity(); u = User.query.get(idt.get('id'))
    ts = Ticket.query.filter((Ticket.owner_email==u.email)|(Ticket.owner_name==u.name)).all()
    return jsonify({'status':'ok','tickets':[{'id':t.id,'zone':t.zone,'used':t.used} for t in ts]})

@bp.route('/api/scan', methods=['POST'])
@jwt_required()
def scan():
    idt = get_jwt_identity()
    if idt.get('role') not in ['scanner','admin','manager']: return jsonify({'status':'error','message':'forbidden'}),403
    t = Ticket.query.filter_by(id=request.json.get('ticket_id')).first()
    if not t: return jsonify({'status':'error','message':'notfound'}),404
    if t.used: return jsonify({'status':'error','message':'used'}),400
    t.used=True; db.session.commit()
    return jsonify({'status':'ok','ticket':{'id':t.id,'used':t.used}})

@bp.route('/api/stats', methods=['GET'])
@jwt_required()
def stats():
    idt = get_jwt_identity()
    if idt.get('role')!='admin': return jsonify({'status':'error','message':'forbidden'}),403
    ev = Event.query.first()
    sold = Ticket.query.filter_by(event_id=ev.id).count() if ev else 0
    used = Ticket.query.filter_by(event_id=ev.id, used=True).count() if ev else 0
    zones = {z: Ticket.query.filter_by(event_id=ev.id, zone=z).count() for z in (ev.zones.keys() if ev else [])} if ev else {}
    return jsonify({'status':'ok','stats':{'sold':sold,'used':used,'capacity':ev.capacity if ev else 0,'zones':zones}})
