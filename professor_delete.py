from flask import Blueprint, jsonify
from utils import connect_to_database

professor_delete_bp = Blueprint('professor_delete_bp', __name__)

@professor_delete_bp.route('/professor_delete/<int:idusuario>', methods=['DELETE'])
def professor_delete(idusuario):
    try:
        with connect_to_database() as db:
            cursor = db.cursor()

            cursor.execute("DELETE FROM professor WHERE idusuario = %s", (idusuario,))
           
            db.commit()

            if cursor.rowcount == 0:
                return jsonify({'mensagem': 'Nenhum professor encontrado com este ID.'}), 404

            return jsonify({'mensagem': 'Professor excluído com sucesso!'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
                        