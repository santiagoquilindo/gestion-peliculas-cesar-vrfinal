from flask import render_template, request, redirect, url_for, flash
from models.usuario import Usuario
from werkzeug.security import generate_password_hash
from app import app
from flask import session
from werkzeug.security import generate_password_hash
from flask_mail import Message, Mail
import secrets

mail = Mail(app)
@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        correo = request.form.get('correo')
        usuario = Usuario.objects(correo=correo).first()
        if not usuario:
            flash("Correo no registrado", "error")
            return redirect(url_for('recuperar'))
        token = secrets.token_urlsafe(32)
        usuario.token = token
        usuario.save()
        enlace = url_for('resetear', token=token, _external=True)
        mensaje = Message("Recuperación de contraseña",recipients=[correo])
        mensaje.body = f"Hola {usuario.nombre}, haz clic en el siguiente enlace para restablecer tu contraseña:\n\n{enlace}\n\nSi no solicitaste esto, ignora el mensaje."
        mail.send(mensaje)
        flash("Se ha enviado un enlace de recuperación a tu correo", "success")
        return redirect(url_for('login'))
    return render_template('recuperarcuenta.html')


@app.route('/resetear/<token>', methods=['GET', 'POST'])
def resetear(token):
    usuario = Usuario.objects(token=token).first()
    if not usuario:
        flash("Token inválido o expirado", "error")
        return redirect(url_for('login'))
    if request.method == 'POST':
        nueva = request.form.get('nueva')
        usuario.password = generate_password_hash(nueva)
        usuario.token = None 
        usuario.save()
        flash("Contraseña actualizada correctamente", "success")
        return redirect(url_for('login'))

    return render_template('cambiarclave.html')