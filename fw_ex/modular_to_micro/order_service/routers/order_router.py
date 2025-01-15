from fastapi import APIRouter, HTTPException
from redis import Redis
import json
import asyncio
from fastapi import Depends

router = APIRouter()
redis_client = Redis(host='redis', port=6379, decode_responses=True)

@router.post("/")
async def create_order(order: OrderRequest, user_req: UserRequest):
    # First check user in cache
    cached_user = redis_client.get(f"user:{user_req.username}")
    
    if not cached_user:
        # If not in cache, verify through user service
        redis_client.publish('verify_user', json.dumps({'user_id': user_req.username}))
        
        # Wait for response with timeout
        pubsub = redis_client.pubsub()
        pubsub.subscribe('user_verification_response')
        
        for _ in range(50):
            message = pubsub.get_message()
            if message and message['type'] == 'message':
                response = json.loads(message['data'])
                if not response['is_valid']:
                    raise HTTPException(status_code=404, detail="User not found")
                break
            await asyncio.sleep(0.1)
    
    # Create order logic here
    db = Depends(get_db)
    order_data = place_order(db, user_req.username, order.item)
    return OrderResponse(
        order_id=order_data.id,
        user=user_req.username,
        item=order.item
    )

# When user is updated
redis_client.publish('user_updates', json.dumps({
    'event': 'user_updated',
    'user_id': user_id,
    'data': updated_data
})) 