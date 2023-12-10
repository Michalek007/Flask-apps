"""
Each blueprint structure:
- modules -> classes, handlers, helpers etc.
- templates/blueprint -> html, css, js files
- __init__.py -> blueprint declaration
- blueprint_class.py -> BlueprintClass declaration ( implements singleton and methods for endpoints )
- views.py -> endpoints methods declaration (invokes BlueprintClass methods)
"""
from app import login_manager
from app.blueprints.bp_singleton import BlueprintSingleton
