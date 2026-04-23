from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models import User, Task

# --- AUTHENTICATION RESOURCES ---

class Signup(Resource):
    def post(self):
        data = request.get_json()
        try:
            # Create user; hashing happens via the @password_hash.setter in models.py
            new_user = User(username=data.get('username'))
            new_user.password_hash = data.get('password')
            
            db.session.add(new_user)
            db.session.commit()
            
            # Auto-login after signup
            session['user_id'] = new_user.id
            return new_user.to_dict(), 201
        except Exception as e:
            return {"errors": ["Username already taken or invalid data"]}, 422

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        
        if user and user.authenticate(data.get('password')):
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {"errors": ["Invalid username or password"]}, 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            return user.to_dict(), 200
        return {"message": "Not logged in"}, 401


# --- TASK RESOURCES (WITH PAGINATION) ---

class Tasks(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401
        
        # Pagination: reads ?page=X from URL, defaults to 1
        page = request.args.get('page', 1, type=int)
        per_page = 10 
        
        tasks_pagination = Task.query.filter_by(user_id=user_id).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            "tasks": [t.to_dict() for t in tasks_pagination.items],
            "total_tasks": tasks_pagination.total,
            "current_page": tasks_pagination.page,
            "total_pages": tasks_pagination.pages
        }, 200

    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401
            
        data = request.get_json()
        try:
            new_task = Task(
                title=data.get('title'),
                description=data.get('description'),
                importance=data.get('importance'),
                user_id=user_id
            )
            db.session.add(new_task)
            db.session.commit()
            return new_task.to_dict(), 201
        except Exception as e:
            return {"errors": [str(e)]}, 400

class TaskByID(Resource):
    def patch(self, id):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401
            
        task = Task.query.filter_by(id=id, user_id=user_id).first()
        if not task:
            return {"error": "Task not found"}, 404
            
        data = request.get_json()
        for attr in data:
            setattr(task, attr, data[attr])
        
        db.session.commit()
        return task.to_dict(), 200

    def delete(self, id):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401
            
        task = Task.query.filter_by(id=id, user_id=user_id).first()
        if not task:
            return {"error": "Task not found"}, 404
            
        db.session.delete(task)
        db.session.commit()
        return {}, 204

# --- ROUTE REGISTRATION ---

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Tasks, '/tasks')
api.add_resource(TaskByID, '/tasks/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)