from config import app, db
from models import User, Task
from faker import Faker
import random

fake = Faker()

def run_seed():
    with app.app_context():
        print("--- Starting Seed ---")
        
        print("Cleaning out old data...")
        Task.query.delete()
        User.query.delete()

        print("Generating 5 random users...")
        users = []
        for _ in range(5):
            u = User(username=fake.user_name().lower())
            # This triggers our @password_hash.setter in models.py
            u.password_hash = 'password123'
            users.append(u)
            db.session.add(u)

        print("Generating 15 tasks...")
        tasks_list = ["Finish Lab", "Buy Groceries", "Study Python", "Clean Room", "Workout"]
        for _ in range(15):
            t = Task(
                title=random.choice(tasks_list),
                description=fake.sentence(),
                importance=random.randint(1, 5),
                user=random.choice(users)
            )
            db.session.add(t)

        db.session.commit()
        print("--- Success: Database is Seeded! ---")

if __name__ == '__main__':
    run_seed()