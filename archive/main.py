# main.py
from fastapi import FastAPI, HTTPException, Query, Depends, Header, HTTPException
from User import UserCreate, UserPublic, User
from Book import Book
from typing import Optional, Annotated
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    EDITOR = "editor"

app = FastAPI()

# In-memory storage for demonstration
users_db = {
    1: UserPublic(id=1, name="John Doe", email="john.doe@example.com", age=25, min_age=18, role=UserRole.ADMIN),
    2: UserPublic(id=2, name="Jane Smith", email="jane.smith@example.com", age=22, min_age=18, role=UserRole.USER),
    3: UserPublic(id=3, name="Jim Beam", email="jim.beam@example.com", age=30, min_age=18, role=UserRole.USER),
    4: UserPublic(id=4, name="Jill Johnson", email="jill.johnson@example.com", age=28, min_age=18, role=UserRole.EDITOR),
    5: UserPublic(id=5, name="Jack Daniels", email="jack.daniels@example.com", age=32, min_age=18, role=UserRole.USER),
    6: UserPublic(id=6, name="Jill Johnson", email="jill.johnson@example.com", age=28, min_age=18, role=UserRole.USER),
    7: UserPublic(id=7, name="Jack Daniels", email="jack.daniels@example.com", age=32, min_age=18, role=UserRole.USER),
}
books_db = {}

@app.get("/hello/{name}")
async def say_hello(name: str = 'World'):
    return {"message": f"Hello, {name}!"}

@app.post("/user", response_model=UserPublic)
async def create_user(user: UserCreate):
    # Store the user in our database. 
    # DO NOT need to instantiate the UserCreate class.
    users_db[user.id] = user
    
    # Convert to public version for response
    user_public = UserPublic.model_validate(user)
    return user_public


@app.get("/users", response_model=list[UserPublic])
async def get_users_based_on_condition(
    min_age: Annotated[Optional[int], Query(description="Minimum age filter")] = None, 
    role: Annotated[Optional[UserRole], Query(description="Role filter")] = None
):
    qualified_users = []
    
    for user in users_db.values():
        # Check if user meets the criteria
        meets_age_criteria = min_age is None or user.age >= min_age if user.age else False
        meets_role_criteria = role is None or user.role == role if hasattr(user, 'role') else True
        
        if meets_age_criteria and meets_role_criteria:
            qualified_users.append(UserPublic.model_validate(user))
    
    return qualified_users


@app.get("/search", response_model=list[UserPublic])
async def search(
    q: Annotated[str, Query()] = None,
    limit: Annotated[int, Query()] = 10,
    offset: Annotated[int, Query()] = 0,
    sort_by: Annotated[str, Query()] = "name",
):
    search_results = users_db.values()
    if q:
        search_results = [user for user in search_results if q.lower() in user.name.lower()]
    if sort_by:
        search_results = sorted(search_results, key=lambda x: getattr(x, sort_by))
    if limit:
        search_results = search_results[:limit]
    if offset:
        search_results = search_results[offset:offset+limit]
    return search_results

        

@app.get("/user_fields")
async def user_fields(user: UserCreate):
    user_fields = user.model_json_schema()
    return user_fields

# Add a GET endpoint to retrieve users
@app.get("/user/{user_id}", response_model=UserPublic)
async def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return UserPublic.model_validate(users_db[user_id])


@app.post("/book", response_model=Book)
async def create_book(book: Book):
    # Store the book in our database. 
    # DO NOT need to instantiate the Book class.
    books_db[book.id] = book
    
    # Convert to public version for response
    book_public = Book.model_validate(book)
    return book_public

async def get_token_header(x_token: Annotated[str, Header()]):
    accepted_tokens = ["admin-token", "user-token"]
    if x_token not in accepted_tokens:
      raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token

@app.get("/protected_user", response_model=UserPublic)
async def get_protected_user(token: Annotated[str, Depends(get_token_header)]):
    return UserPublic(id=1, name="John Doe", email="john.doe@example.com", age=25, min_age=18, role=UserRole.ADMIN)

@app.get("/status")
async def status(feeling: str = 'OK', is_asked: bool = False, user: UserPublic = Depends(get_protected_user)):
    if is_asked:
        return {"message": f"{user.name} is feeling {feeling}!"}
    else:
        return {"message": f"{user.name} is not feeling anything."}

@app.get("/header")
async def header(user_agent: Annotated[str, Header()]):
    return {"user_agent": user_agent}


async def get_current_user(token: Annotated[str, Depends(get_token_header)]):
    print(token)
    if token == "admin-token":
        return User(id=1, name="admin", role="admin", email="admin@example.com")
    elif token == "user-token":
        return User(id=2, name="user", role="user", email="user@example.com")
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/me", response_model=User)
async def me(user: User = Depends(get_current_user)):
    return user

def admin_required(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    return user

@app.delete("/delete-data")
def delete_data(dep: None = Depends(admin_required)):
    return {"status": "deleted"}