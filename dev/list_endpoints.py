from main import app

for route in app.routes:
    methods = ','.join(route.methods)
    print(f"{methods:10} {route.path}")