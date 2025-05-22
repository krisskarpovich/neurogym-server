from datetime import datetime, timedelta

# def save_token(db, user_id, token: str):
#     expires_at = datetime.utcnow() + timedelta(minutes=100)  # например, 1 час
#     token_entry = Token(
#         access_token=token,
#         user_id=user_id,
#         created_at=datetime.utcnow(),
#         expires_at=expires_at,
#     )
#     db.add(token_entry)
#     db.commit()
#     db.refresh(token_entry)
#     return token_entry
