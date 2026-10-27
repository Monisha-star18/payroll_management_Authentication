from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.Table_Model import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, 
                                    primary_key=True, 
                                    autoincrement=True
                                    )
    
    username: Mapped[str] = mapped_column(String(50), 
                                          unique=True, 
                                          nullable=False
                                        )
    
    hashed_password: Mapped[str] = mapped_column(String(255),
                                                nullable=False
                                                )
    
    role: Mapped[str] = mapped_column(String(10), 
                                      nullable=False,
                                      default="user", 
                                      server_default="user"
                                    )