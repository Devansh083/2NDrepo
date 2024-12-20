from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pubchempy as pcp
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chemicals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Chemical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    molecular_formula = db.Column(db.String(100))
    molecular_weight = db.Column(db.Float)
    smiles = db.Column(db.String(200))
with app.app_context():
    db.create_all()
@app.route('/fetch', methods=['POST'])
def fetch_chemical_data():
    data = request.json
    substance1 = data.get('substance1')
    substance2 = data.get('substance2')

    def get_chemical_info(substance):
        """Fetch chemical information from PubChem."""
        try:
            compound = pcp.get_compounds(substance, 'name')[0]
            return {
                "name": substance,
                "molecular_formula": compound.molecular_formula,
                "molecular_weight": compound.molecular_weight,
                "smiles": compound.canonical_smiles
            }
        except IndexError:
            return None

    chemical1 = get_chemical_info(substance1)
    chemical2 = get_chemical_info(substance2)

    if chemical1 and chemical2:
        for chemical in [chemical1, chemical2]:
            if not Chemical.query.filter_by(name=chemical['name']).first():
                db.session.add(Chemical(
                    name=chemical['name'],
                    molecular_formula=chemical['molecular_formula'],
                    molecular_weight=chemical['molecular_weight'],
                    smiles=chemical['smiles']
                ))
        db.session.commit()

        return jsonify({
            "substance1": chemical1,
            "substance2": chemical2,
            "reaction": f"{chemical1['name']} reacts with {chemical2['name']} to form products."
        })

    return jsonify({"error": "Substance(s) not found in PubChem"}), 404

if __name__ == '__main__':
    app.run(debug=True)
