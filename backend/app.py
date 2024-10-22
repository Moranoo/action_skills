from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from bson.objectid import ObjectId
from bson.errors import InvalidId
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# Connexion à MongoDB
client = MongoClient(os.getenv('MONGO_URI'))
db = client.evenementsDB

@app.route('/')
def home():
    return "Bienvenue sur la plateforme de gestion d'événements!"

@app.route('/evenements', methods=['GET'])
def get_evenements():
    evenements = db.evenements.find()
    result = []
    for evenement in evenements:
        result.append({
            'titre': evenement['titre'],
            'date': evenement['date'],
            'lieu': evenement['lieu'],
            'description': evenement['description']
        })
    return jsonify(result)

@app.route('/utilisateurs', methods=['GET'])
def get_utilisateurs():
    utilisateurs = db.utilisateurs.find()
    result = []
    for utilisateur in utilisateurs:
        result.append({'nom': utilisateur['nom'], 'email': utilisateur['email']})
    return jsonify(result)

@app.route('/utilisateurs/multiple', methods=['POST'])
def add_multiple_utilisateurs():
    data = request.get_json()  # On attend un tableau JSON
    if isinstance(data, list):
        for utilisateur in data:
            nom = utilisateur.get('nom')
            email = utilisateur.get('email')

            if nom and email:
                db.utilisateurs.insert_one({'nom': nom, 'email': email})
            else:
                return jsonify({'message': 'Données invalides dans un des objets'}), 400

        return jsonify({'message': 'Utilisateurs ajoutés avec succès!'}), 201
    else:
        return jsonify({'message': 'Les données envoyées ne sont pas sous forme de tableau'}), 400

@app.route('/evenements/multiple', methods=['POST'])
def add_multiple_evenements():
    data = request.get_json()  # On attend un tableau JSON
    if isinstance(data, list):
        for evenement in data:
            titre = evenement.get('titre')
            date = evenement.get('date')
            lieu = evenement.get('lieu')
            description = evenement.get('description')

            if titre and date and lieu and description:
                db.evenements.insert_one({
                    'titre': titre,
                    'date': date,
                    'lieu': lieu,
                    'description': description
                })
            else:
                return jsonify({'message': 'Données invalides dans un des objets'}), 400

        return jsonify({'message': 'Événements ajoutés avec succès!'}), 201
    else:
        return jsonify({'message': 'Les données envoyées ne sont pas sous forme de tableau'}), 400

#route permettra à un utilisateur de s'inscrire à un événement en fournissant son ID utilisateur et l'ID de l'événement.
@app.route('/inscription', methods=['POST'])
def inscrire_utilisateur():
    data = request.get_json()
    utilisateur_id = data.get('utilisateur_id')
    evenement_id = data.get('evenement_id')

    # Vérifier si les deux ID sont fournis
    if not utilisateur_id or not evenement_id:
        return jsonify({'message': 'Veuillez fournir un utilisateur_id et un evenement_id.'}), 400

    # Vérifier la validité des ObjectIds
    try:
        utilisateur_obj_id = ObjectId(utilisateur_id)
        evenement_obj_id = ObjectId(evenement_id)
    except InvalidId:
        return jsonify({'message': 'ID utilisateur ou ID événement non valide.'}), 400

    # Vérifier si l'utilisateur existe
    utilisateur = db.utilisateurs.find_one({'_id': utilisateur_obj_id})
    if not utilisateur:
        return jsonify({'message': 'Utilisateur non trouvé.'}), 404

    # Vérifier si l'événement existe
    evenement = db.evenements.find_one({'_id': evenement_obj_id})
    if not evenement:
        return jsonify({'message': 'Événement non trouvé.'}), 404

    # Vérifier si l'utilisateur est déjà inscrit à cet événement
    inscription_existante = db.inscriptions.find_one({
        'utilisateur_id': utilisateur_obj_id,
        'evenement_id': evenement_obj_id
    })

    if inscription_existante:
        return jsonify({'message': 'L\'utilisateur est déjà inscrit à cet événement.'}), 409

    # Inscrire l'utilisateur à l'événement
    inscription = {
        'utilisateur_id': utilisateur_obj_id,
        'evenement_id': evenement_obj_id,
        'date_inscription': datetime.now().strftime('%Y-%m-%d')
    }
    db.inscriptions.insert_one(inscription)

    return jsonify({'message': 'Inscription réussie!'}), 201

@app.route('/inscriptions/<utilisateur_id>', methods=['GET'])
def get_inscriptions(utilisateur_id):
    try:
        utilisateur_obj_id = ObjectId(utilisateur_id)
    except:
        return jsonify({'message': 'ID utilisateur non valide.'}), 400

    # Trouver toutes les inscriptions pour cet utilisateur
    inscriptions = db.inscriptions.find({'utilisateur_id': utilisateur_obj_id})
    result = []
    
    for inscription in inscriptions:
        # Trouver les détails de l'événement pour chaque inscription
        evenement = db.evenements.find_one({'_id': inscription['evenement_id']})
        if evenement:
            result.append({
                'titre': evenement['titre'],
                'date': evenement['date'],
                'lieu': evenement['lieu'],
                'description': evenement['description'],
                'date_inscription': inscription['date_inscription']
            })

    if not result:
        return jsonify({'message': 'Aucune inscription trouvée pour cet utilisateur.'}), 404

    return jsonify(result), 200

@app.route('/inscription/<inscription_id>', methods=['DELETE'])
def delete_inscription(inscription_id):
    try:
        inscription_obj_id = ObjectId(inscription_id)
    except:
        return jsonify({'message': 'ID d\'inscription non valide.'}), 400

    # Vérifier si l'inscription existe
    inscription = db.inscriptions.find_one({'_id': inscription_obj_id})
    if not inscription:
        return jsonify({'message': 'Inscription non trouvée.'}), 404

    # Supprimer l'inscription
    db.inscriptions.delete_one({'_id': inscription_obj_id})
    
    return jsonify({'message': 'Inscription annulée avec succès.'}), 200

@app.route('/evenement/<id>', methods=['GET'])
def get_evenement(id):
    try:
        # Convertir l'ID en ObjectId pour MongoDB
        evenement_obj_id = ObjectId(id)
    except InvalidId:
        return jsonify({'message': 'ID événement non valide.'}), 400

    # Trouver l'événement correspondant dans la base de données
    evenement = db.evenements.find_one({'_id': evenement_obj_id})

    if not evenement:
        return jsonify({'message': 'Événement non trouvé.'}), 404

    # Retourner les détails de l'événement
    return jsonify({
        'titre': evenement['titre'],
        'date': evenement['date'],
        'lieu': evenement['lieu'],
        'description': evenement['description']
    }), 200

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello from the backend!'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
