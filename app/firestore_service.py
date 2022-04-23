import firebase_admin
from firebase_admin import credentials, firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()


def register_user(user_data):
    """
    :param user_data: UserData
    """
    user_ref = db.document(f'users/{user_data.username}')
    user_ref.set({'password': user_data.password})


def get_all_users():
    return db.collection('users').get()


def get_user(user_id):
    return db.document(f'users/{user_id}').get()


def add_todo(user_id, description):
    db.collection(f'users/{user_id}/todos').add({
        'description': description,
        'done': False
        }
    )


def get_todos(user_id):
    return db.collection(f'users/{user_id}/todos').get()


def delete_todo(user_id, todo_id):
    _get_todo_ref(user_id, todo_id).delete()


def toggle_complete_todo(user_id, todo_id):
    todo = _get_todo_ref(user_id, todo_id)
    
    if todo.get().to_dict()['done']:
        todo.update({'done': False})
    else:
        todo.update({'done': True})


def _get_todo_ref(user_id, todo_id):
    return db.document(f'users/{user_id}/todos/{todo_id}')