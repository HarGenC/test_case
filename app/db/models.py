import uuid
from typing import Annotated

from sqlalchemy import UUID, CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


uuid_pk = Annotated[uuid.UUID, 
                    mapped_column(UUID(as_uuid=True), 
                    primary_key=True, 
                    server_default=text('gen_random_uuid()'))]

class WalletsOrm(Base):
    __tablename__="wallets"

    uuid: Mapped[uuid_pk]
    balance: Mapped[int] = mapped_column(nullable=False, server_default='0')
    
    __table_args__ = (
        CheckConstraint('balance >= 0', name='balance_non_negative'),
    )
