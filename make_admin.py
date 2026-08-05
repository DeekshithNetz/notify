from database import SessionLocal
import models

db = SessionLocal()


def make_admin():
    email = input("Enter user email: ")

    user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    if user:
        user.role = "admin"
        db.commit()
        print("\n✅ Admin updated successfully.")
    else:
        print("\n❌ User not found.")


def show_all_users():
    users = db.query(models.User).all()

    if not users:
        print("\nNo users found.")
        return

    print("\n========== USERS ==========")

    for user in users:
        print(f"ID         : {user.id}")
        print(f"Name       : {user.name}")
        print(f"Email      : {user.email}")
        print(f"Google ID  : {user.google_id}")
        print(f"Role       : {user.role}")
        print(f"FCM Token  : {user.fcm_token}")
        print("-" * 40)


while True:
    print("\n========== MENU ==========")
    print("1. Make Admin")
    print("2. Show All Users")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        make_admin()

    elif choice == "2":
        show_all_users()

    elif choice == "3":
        db.close()
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")