from fastapi import APIRouter

router = APIRouter()

@router.get('/test')
async def test():
    return {"message": "Hello world"}

@router.get('/test1')
async def test():
    return {"message": "Hello world"}

@router.get('/test2')
async def test():
    return {"message": "Hello world"}

@router.get('/test3')
async def test():
    return {"message": "Hello world"}