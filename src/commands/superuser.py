import click
from flask import current_app
from flask.cli import with_appcontext
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from src.database.db import session_scope
from src.database.models import User, Role
from src.schemas.users import UserCreateSchema


@click.command(name="create-superuser")
@click.argument("login")
@click.argument("password")
@with_appcontext
def create_superuser(login: str, password: str):
    with session_scope() as session:
        try:
            raw_user = User(login=login, password=password, is_admin=True)
            UserCreateSchema.from_orm(raw_user)
        except ValidationError:
            raise click.ClickException("Invalid arguments.")
        try:
            admin_role_id, _ = session.query(Role).filter_by(permissions=0xff).with_entities(Role.id).first()
            raw_user.role_id = admin_role_id
            session.add(raw_user)
            session.commit()
            current_app.logger.info("Superuser successfully created")
        except IntegrityError:
            session.rollback()
            current_app.logger.info("Such user exists")
