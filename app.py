from flask import Flask, jsonify, render_template, request, redirect, url_for
import mysql.connector

from aluno_update import aluno_update_bp


app = Flask(__name__)


app.register_blueprint(aluno_update_bp)


if __name__ == '__main__':
    app.run(debug=True)
