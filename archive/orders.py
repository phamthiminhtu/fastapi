from fastapi import APIRouter

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@router.get("/")
def get_orders():
    return {"orders": ["order1", "order2", "order3"]}

@router.post("/")
def create_order():
    return {"message": "Order created successfully"}

@router.get("/{order_id}")
def get_order(order_id: int):
    return {"order_id": order_id, "status": "pending"}