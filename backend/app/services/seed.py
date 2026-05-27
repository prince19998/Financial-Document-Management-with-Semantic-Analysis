from sqlalchemy.orm import Session

from app.auth.security import hash_password
from app.models.entities import Permission, Role, User

DEFAULT_PERMISSIONS = [
    ("admin:*", "Full platform access"),
    ("documents:upload", "Upload financial documents"),
    ("documents:edit", "Edit document metadata"),
    ("documents:view", "View company documents"),
    ("documents:delete", "Delete documents"),
    ("documents:review", "Review documents"),
    ("rag:search", "Use semantic search and RAG"),
    ("users:manage", "Manage users and roles"),
]

DEFAULT_ROLES = {
    "Admin": ["admin:*"],
    "Financial Analyst": ["documents:upload", "documents:edit", "documents:view", "rag:search"],
    "Auditor": ["documents:view", "documents:review", "rag:search"],
    "Client": ["documents:view", "rag:search"],
}


def seed_defaults(db: Session) -> None:
    permission_map = {}
    for code, description in DEFAULT_PERMISSIONS:
        permission = db.query(Permission).filter_by(code=code).first()
        if not permission:
            permission = Permission(code=code, description=description)
            db.add(permission)
        permission_map[code] = permission

    for role_name, permissions in DEFAULT_ROLES.items():
        role = db.query(Role).filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name, description=f"Default {role_name} role")
            db.add(role)
        role.permissions = [permission_map[code] for code in permissions]
    db.commit()

    admin = db.query(User).filter_by(email="admin@example.com").first()
    if not admin:
        admin = User(email="admin@example.com", full_name="Platform Admin", hashed_password=hash_password("Admin@123"))
        admin.roles = [db.query(Role).filter_by(name="Admin").one()]
        db.add(admin)

    db.commit()
