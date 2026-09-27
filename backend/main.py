import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
# Conexion a MySQL
DB_USER = os.getenv("MYSQL_USER", "user")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
DB_HOST = os.getenv("MYSQL_HOST", "db")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE", "mi_base")
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# SQLAlchemy (ORM)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# Modelo para tabla "usuarios"
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
app = FastAPI(title="Backend FastAPI - Gestión Usuarios")
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": f'FastAPI corriendo en puerto{DB_PORT}'}
@app.get("/api/usuarios")
def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return [
        {
            "id": u.id,
            "nombre": u.nombre, 
            "email": u.email
            } 
            for u in usuarios
            ]
@app.get("/api/bienvenida")
def obtener_bienvenida(db: Session = Depends(get_db)):
    # Toma el primer usuario para mostrar el mensaje de bienvenida
    primer_usuario = db.query(Usuario).first()
    if not primer_usuario:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")
    return {
        "mensaje": f"¡Bienvenido/a {primer_usuario.nombre}!",
        "usuario": {
            "id": primer_usuario.id,
            "nombre": primer_usuario.nombre,
            "email": primer_usuario.email
        }
    }