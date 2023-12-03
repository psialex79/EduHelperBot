from .addteacher import router as addteacher_router

def get_admin_routers():
    return [addteacher_router]