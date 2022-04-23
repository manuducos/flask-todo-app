# Python
import unittest

# Flask and extensions
from flask import request, redirect, session, url_for
from flask import render_template
from flask_login import login_required, current_user

# Internal
from app import create_app
from app.firestore_service import get_todos, add_todo, delete_todo, toggle_complete_todo
from app.forms import ToDoForm


app = create_app()


@app.route('/')
def index():
    if current_user.is_authenticated:
        user_ip = request.remote_addr
        session['user_ip'] = user_ip

        return redirect(url_for('hello'))
    
    return redirect(url_for('auth.login'))



@app.route(
    '/hello',
    methods=['GET', 'POST']
    )
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = ToDoForm()

    if todo_form.validate_on_submit():
        new_todo = todo_form.description.data
        add_todo(username, new_todo)

    todos = [todo for todo in get_todos(username)]

    context = {
        'user_ip': user_ip, 
        'todos': todos,
        'username': username,
        'todo_form': todo_form,
    }

    if user_ip:
        return render_template('hello.html', **context)
    else:
        return redirect(url_for('index'))


@app.route('/todos/delete/<todo_id>')
def delete(todo_id):
    username = current_user.id
    delete_todo(username, todo_id)
    return redirect(url_for('hello'))


@app.route('/todos/toggle_complete_todo/<todo_id>')
def toggle_complete(todo_id):
    username = current_user.id
    toggle_complete_todo(username, todo_id)
    return redirect(url_for('hello'))


@app.route('/todos/clear-completed')
def clear():
    username = current_user.id
    todos = [todo for todo in get_todos(username)]

    for todo in todos:
        if todo.to_dict()['done']:
            delete_todo(username, todo.id)
    
    return redirect(url_for('hello'))


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.route('/internal-error')
def raise_internal_error():
    return 1 / 0


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)