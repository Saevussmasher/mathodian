import os
from flask import Flask, jsonify, request, render_template, send_from_directory
from api.operation_registry import registry
import api.operations  # Triggers auto-discovery
import importlib
import pkgutil

# Auto-load all operation modules
def load_operations():
    import api.operations
    registry.load_operations(api.operations)

load_operations()

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/operation/<operation_id>")
def operation_page(operation_id):
    op_cls = registry.get_operation(operation_id)
    if not op_cls:
        return "Operation not found", 404
    return render_template("operation.html", operation=op_cls.metadata())

@app.route("/api/operations")
def api_list_operations():
    return jsonify(registry.list_operations())

@app.route("/api/operations/<operation_id>")
def api_operation_metadata(operation_id):
    op_cls = registry.get_operation(operation_id)
    if not op_cls:
        return jsonify({"error": "Operation not found"}), 404
    return jsonify(op_cls.metadata())

@app.route("/api/operations/<operation_id>/calculate", methods=["POST"])
def api_operation_calculate(operation_id):
    op_cls = registry.get_operation(operation_id)
    if not op_cls:
        return jsonify({"error": "Operation not found"}), 404
    # Validate and parse parameters
    try:
        input_data = request.json
        params = {}
        for param in op_cls.parameters():
            value = input_data.get(param.name)
            params[param.name] = param.validate(value)
        result = op_cls.calculate(params)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# Serve static files (JS, CSS)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)