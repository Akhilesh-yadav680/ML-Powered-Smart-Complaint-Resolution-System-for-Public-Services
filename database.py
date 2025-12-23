import os
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# ===== ABSOLUTE DATABASE PATH =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "complaints.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# ================= USER TABLE =================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)  # admin / citizen

    complaints = relationship("Complaint", back_populates="user")

# ================= COMPLAINT TABLE =================
class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    category = Column(String(50))
    priority = Column(String(20))
    status = Column(String(20), default="Pending")
    location = Column(String(120), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="complaints")

# ================= CREATE TABLES =================
Base.metadata.create_all(engine)

# ================= CREATE DEFAULT ADMIN =================
if not session.query(User).filter_by(username="admin").first():
    admin = User(
        username="admin",
        password="admin",   # (we’ll hash later if needed)
        role="admin"
    )
    session.add(admin)
    session.commit()
    print("✅ Default admin created (username=admin, password=admin)")

print("✅ Database ready at:", DB_PATH)
