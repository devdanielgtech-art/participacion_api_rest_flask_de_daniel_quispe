from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Crear base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///peliculas_de_daniel.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Pelicula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    calificacion = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "calificacion": self.calificacion
        }


# Rutas
@app.route("/")
def home():
    return jsonify({"message": "Bienvenido al sistema de gestion de peliculas de DANIEL QUISPE GUTIERREZ!!!"})

# Obtiene lista de películas en formato JSON
@app.route("/peliculas", methods=["GET"])
def get_peliculas():
    peliculas = Pelicula.query.all()
    return jsonify([pelicula.to_dict() for pelicula in peliculas])

# Obtener una película en formato JSON a partir del id
@app.route("/peliculas/<int:id>", methods=["GET"])
def get_pelicula(id):
    obj_pelicula = Pelicula.query.get(id)
    if obj_pelicula:
        return jsonify(obj_pelicula.to_dict())
    else:
        return jsonify({"error": "No existe la película solicitada"}), 400

# Adición de un registro enviado mediante JSON
@app.route("/peliculas", methods=["POST"])
def add_pelicula():
    data = request.get_json()
    objnew = Pelicula(
        titulo=data["titulo"],
        genero=data["genero"],
        calificacion=data["calificacion"]
    )
    db.session.add(objnew)
    db.session.commit()
    return jsonify(objnew.to_dict()), 201

# Actualización de un registro enviado mediante JSON y un id
@app.route("/peliculas/<int:id>", methods=["PUT"])
def update_pelicula(id):
    data = request.get_json()
    obj_pelicula = Pelicula.query.get(id)
    if obj_pelicula:
        obj_pelicula.titulo = data.get("titulo")
        obj_pelicula.genero = data.get("genero")
        obj_pelicula.calificacion = data.get("calificacion")
        
        db.session.commit()
        return jsonify(obj_pelicula.to_dict())
    else:
        return jsonify({"error": "No existe la película para actualizar"}), 400

# Eliminación de un registro
@app.route("/peliculas/<int:id>", methods=["DELETE"])
def delete_pelicula(id):
    obj_pelicula = Pelicula.query.get(id)
    if obj_pelicula:
        db.session.delete(obj_pelicula)
        db.session.commit()
        return jsonify({"message": "Película eliminada"})
    else:
        return jsonify({"error": "No existe película para eliminar"}), 400

# Iniciar la aplicación
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)