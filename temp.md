flask db init
flask db migrate -m "initial migration"
flask db upgrade

flask shell

> > > from app import db
> > > from app.models import User
> > > admin = User(username='admin', email='admin@example.com', is_admin=True)
> > > admin.set_password('admin123')
> > > db.session.add(admin)
> > > db.session.commit()
