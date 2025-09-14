# LibraryProject – Permissions and Groups Setup

## Custom Permissions
Defined in `bookshelf/models.py` on the `Book` model:

- `can_view` – Can view book
- `can_create` – Can create book
- `can_edit` – Can edit book
- `can_delete` – Can delete book

These permissions are created automatically when running:
```bash
python manage.py makemigrations bookshelf
python manage.py migrate
