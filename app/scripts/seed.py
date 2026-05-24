import app.models
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password


def seed_users():
    db: Session = SessionLocal()
    
    try:
        # Check if users already exist
        admin_exists = db.query(User).filter(User.email == "admin@creavo.com").first()
        content_exists = db.query(User).filter(User.email == "content@creavo.com").first()
        sales_exists = db.query(User).filter(User.email == "sales@creavo.com").first()
        
        # Hash passwords once and check length
        admin_pwd = hash_password("admin123")
        content_pwd = hash_password("content123") 
        sales_pwd = hash_password("sales123")
        
        print(f"Admin hash length: {len(admin_pwd)}")
        print(f"Content hash length: {len(content_pwd)}")
        print(f"Sales hash length: {len(sales_pwd)}")
        
        # Create admin user
        if not admin_exists:
            admin_user = User(
                email="admin@creavo.com",
                hashed_password=admin_pwd[:72] if len(admin_pwd) > 72 else admin_pwd,
                role="ADMIN",
                full_name="Admin User",
                is_active=True
            )
            db.add(admin_user)
            print("Created admin user")
        
        # Create content user
        if not content_exists:
            content_user = User(
                email="content@creavo.com",
                hashed_password=content_pwd[:72] if len(content_pwd) > 72 else content_pwd,
                role="CONTENT",
                full_name="Content User",
                is_active=True
            )
            db.add(content_user)
            print("Created content user")
        
        # Create sales user
        if not sales_exists:
            sales_user = User(
                email="sales@creavo.com",
                hashed_password=sales_pwd[:72] if len(sales_pwd) > 72 else sales_pwd,
                role="SALES",
                full_name="Sales User",
                is_active=True
            )
            db.add(sales_user)
            print("Created sales user")
        
        # Commit all changes
        db.commit()
        print("Users seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding users: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_users()
    print("Seeding complete")
