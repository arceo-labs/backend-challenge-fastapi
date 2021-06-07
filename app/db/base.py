from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
