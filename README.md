## aximedia_test

### Users [username, email, password]
```
* ["admin", "admin@admin.com", "11223344bb"]
* ["test", "test@test.com", "test1234"]
```

### Organizations [organization_name, id, members]
```
* ["aximedia", 1, admin]
* ["google", 2, (admin, test)]
* ["yandex", 3, test]
```

### Methods available
```
* 'Login'
POST /login application/json {"email": "test@test.com", "password":"test1234", "current_organization_id":2}

* 'Logout' /logout

* 'todos' - all available lists
GET /todos
POST /todos application/json {"name": "New todo list"}

* 'Tasks' add/get tasks to a todo
GET /todos/<todo_id>
POST /todos/<todo_id> application/json {"task_name": "first task"}

* 'Specific task' get/put/delete task
GET /todos/<todo_id>/task/<task_id> 
PUT /todos/<todo_id>/task/<task_id> application/json {"task_name": "modified task"}
DELETE /todos/<todo_id>/task/<task_id> 

```
