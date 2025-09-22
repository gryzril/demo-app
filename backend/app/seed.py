from sqlalchemy import select
from .db import SessionLocal
from .models import Label, User, Role
from hashlib import sha256

# TODO go over this
def run():
    db = SessionLocal()
    try:
        for name in ["work", "home", "urgent"]:
            if not db.scalar(select(Label).where(Label.name == name)):
                db.add(Label(name=name))
        # demo admin
        admin_email = "admin@example.com"
        if not db.scalar(select(User).where(User.email == admin_email)):
            pwd = sha256(b"admin123").hexdigest()  # demo only
            db.add(User(email=admin_email, password_hash=pwd, role=Role.admin))
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    run()
