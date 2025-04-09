from flask import render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from app import app
from models.usuario import Usuario 
import app as dbase
import requests
from correo import enviar_correo_asincrono

# Ruta de Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_input = request.form['usuario']
        contrasena_input = request.form['clave']
        # captcha_response = request.form['g-recaptcha-response']
        # secret_key = "6LenzQ8rAAAAAOAE53gA8-09eiNKNCeStee2Nez-"
        # captcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
        # payload = {'secret': secret_key, 'response': captcha_response}
        # captcha_verification = requests.post(captcha_verify_url, data=payload).json()
        # if not captcha_verification.get('success'):
        #     flash('El CAPTCHA no es valido. Intenta nuevamente.', 'error')
        #     return redirect(url_for('login'))
        usuario_db = Usuario.objects(usuario=usuario_input).first()
        if usuario_db and check_password_hash(usuario_db.password, contrasena_input):
            session['usuario_id'] = str(usuario_db.id)
            session.permanent = True
            flash('Inicio sesion correcto', 'success')
            correo_destino = usuario_db.correo
            asunto = "Inicio de sesión exitoso"
            mensaje = "iniciado sesion correctamente"
            enviar_correo_asincrono(correo_destino, asunto, mensaje)
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas. Intenta nuevamente.', 'error')
            return redirect(url_for('login'))
    return render_template('iniciodesesion.html')

#cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('¡Has cerrado sesión!', 'info')
    return redirect(url_for('login'))
