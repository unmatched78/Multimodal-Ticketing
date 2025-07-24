#main.py
#“app factory” (replaces manage.py/wsgi)
from apps.users.router import router as users_router
app.include_router(users_router)
# Add other routers as needed
# Add CORS middleware, error handlers, etc. as needed
# Add startup and shutdown events if needed
# Add any additional configurations or initializations as needed