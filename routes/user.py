from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ..db import getconnection
from ..services.securite import hashPwd

class UserCreateRequest(BaseModel):
    login: str
    password: str
    Name: str

router = APIRouter()

# GET all
@router.get('/user', status_code=status.HTTP_200_OK)
def getUsers():
    conn = getconnection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, Login, Name, Password FROM USER')
    users = cursor.fetchall()
    conn.close()
    return {'users from db': users}

# GET by id
@router.get('/user/{userID}', status_code=status.HTTP_200_OK)
def getUserID(userID: int):
    conn = getconnection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, Login, Name FROM USER WHERE id = ?', (userID,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {'user': user}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")

# POST create user
@router.post('/user', status_code=status.HTTP_201_CREATED)
def insertUser(user: UserCreateRequest):
    conn = getconnection()
    cursor = conn.cursor()

    # Hash du mot de passe avant insertion
    mdphash = hashPwd(user.password)
    print(f"Mot de passe haché: {mdphash}")

    try:
        cursor.execute(
            'INSERT INTO USER (Login, Password, Name) VALUES (?, ?, ?)',
            (user.login, mdphash, user.Name)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return {"id": user_id}
    except Exception as e:
        print(f"Erreur d'insertion : {str(e)}")
        raise HTTPException(status_code=400, detail="Login déjà utilisé")
    finally:
        conn.close()

# PUT update user
@router.put('/user/{userID}', status_code=status.HTTP_200_OK)
def updateUser(userID: int, user: UserCreateRequest):
    conn = getconnection()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM USER WHERE id = ?', (userID,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")

    mdphash = hashPwd(user.password)

    try:
        cursor.execute(
            'UPDATE USER SET Login = ?, Password = ?, Name = ? WHERE id = ?',
            (user.login, mdphash, user.Name, userID)
        )
        conn.commit()
        return {"message": "put ok"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erreur lors de la mise à jour")
    finally:
        conn.close()

# DELETE user by id
@router.delete('/user/{userID}', status_code=status.HTTP_200_OK)
def deleteUser(userID: int):
    conn = getconnection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM USER WHERE id = ?', (userID,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")

    cursor.execute('DELETE FROM USER WHERE id = ?', (userID,))
    conn.commit()
    conn.close()
    return {"message": "Utilisateur supprimé"}
