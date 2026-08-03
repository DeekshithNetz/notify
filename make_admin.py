from database import SessionLocal
import models


db = SessionLocal()

user = db.query(models.User).filter(
    models.User.email == "deekshithnetz@gmail.com"
).first()


if user:
    user.role = "admin"
    db.commit()
    print("Admin updated")
else:
    print("User not found")


db.close()