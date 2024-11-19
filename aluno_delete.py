from flask import Blueprint, jsonify
from utils import connect_to_database

aluno_delete_bp = Blueprint('aluno_delete_bp', __name__)

@aluno_delete_bp.route('/aluno_delete/<int:idusuario>', methods=['DELETE'])
def usuario_delete(idusuario):
    try:
        with connect_to_database() as db:
            cursor = db.cursor()

            cursor.execute("DELETE FROM aluno WHERE idusuario = %s", (idusuario,))
           
            db.commit()

            if cursor.rowcount == 0:
                return jsonify({'mensagem': 'Aluno usuário encontrado com este ID.'}), 404

            return jsonify({'mensagem': 'Aluno excluído com sucesso!'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
