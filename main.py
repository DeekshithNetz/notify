from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import firebase_service
import models
import schemas
import auth

from database import Base, engine, get_db


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Notification Backend API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "Notification Backend Running"}


@app.post("/google-login", response_model=schemas.Token)
def google_login(
    user: schemas.GoogleLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

  
    if not db_user:
        print("new account ")

        db_user = models.User(
            google_id=user.google_id,
            name=user.name,
            email=user.email
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    print(db_user.role)
    access_token = auth.create_access_token(
        {
            "sub": str(db_user.id),
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "role": db_user.role
        }
    }





@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.get_admin_user)
):
    return db.query(models.User).all()



@app.post("/send-notification")
def send_notification(
        notification: schemas.NotificationRequest,
        admin: models.User = Depends(auth.get_admin_user),
        db: Session = Depends(get_db)
    ):

        users = db.query(models.User).all()

        success = 0
        failed = 0
        print("enterd")

        for user in users:

            if not user.fcm_token:
                continue

            try:

                firebase_service.send_push_notification(
                    token=user.fcm_token,
                    title=notification.title,
                    body=notification.message
                )

                success += 1
                print("sent")


            except Exception as e:
                print(e)
                failed += 1


        return {
            "message": "Notification Process Completed",
            "success": success,
            "failed": failed
        }

    
    
@app.post("/update-fcm-token")
def update_fcm_token(
    data: schemas.UpdateFCMToken,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):

    current_user.fcm_token = data.fcm_token

    db.commit()

    return {
        "message": "FCM Token Updated"
    }