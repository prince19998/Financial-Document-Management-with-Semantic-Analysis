from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import require_permission
from app.database.session import get_db
from app.models.entities import Permission, Role, User
from app.schemas.domain import AssignRoleRequest, RoleCreate

router = APIRouter(tags=["RBAC"])


@router.post("/roles/create")
def create_role(payload: RoleCreate, db: Session = Depends(get_db), _: User = Depends(require_permission("users:manage"))):
    if db.query(Role).filter_by(name=payload.name).first():
        raise HTTPException(status_code=409, detail="Role already exists")
    permissions = []
    for code in payload.permissions:
        permission = db.query(Permission).filter_by(code=code).first()
        if not permission:
            permission = Permission(code=code, description=code.replace(":", " "))
            db.add(permission)
        permissions.append(permission)
    role = Role(name=payload.name, description=payload.description, permissions=permissions)
    db.add(role)
    db.commit()
    return {"id": role.id, "name": role.name, "permissions": [permission.code for permission in role.permissions]}


@router.post("/users/assign-role")
def assign_role(payload: AssignRoleRequest, db: Session = Depends(get_db), _: User = Depends(require_permission("users:manage"))):
    user = db.get(User, payload.user_id)
    role = db.query(Role).filter_by(name=payload.role_name).first()
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or role not found")
    if role not in user.roles:
        user.roles.append(role)
    db.commit()
    return {"message": "Role assigned", "user_id": user.id, "role": role.name}


@router.get("/users/{user_id}/roles")
def user_roles(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_permission("users:manage"))):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.id, "roles": [role.name for role in user.roles]}


@router.get("/users/{user_id}/permissions")
def user_permissions(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_permission("users:manage"))):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    permissions = sorted({permission.code for role in user.roles for permission in role.permissions})
    return {"user_id": user.id, "permissions": permissions}


@router.get("/users")
def list_users(db: Session = Depends(get_db), _: User = Depends(require_permission("users:manage"))):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [{"id": user.id, "email": user.email, "full_name": user.full_name, "roles": [role.name for role in user.roles]} for user in users]


@router.get("/roles")
def list_roles(db: Session = Depends(get_db), _: User = Depends(require_permission("users:manage"))):
    return [{"id": role.id, "name": role.name, "permissions": [permission.code for permission in role.permissions]} for role in db.query(Role).all()]
