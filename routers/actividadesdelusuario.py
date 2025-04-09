from flask import render_template, request, redirect, url_for, flash
from models.usuario import Usuario
from werkzeug.security import generate_password_hash
from app import app
from correo import enviar_correo_asincrono

@app.route('/registrar/', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        data = request.get_json() 
        usuario = data.get('usuario')
        password = data.get('password')
        nombre = data.get('nombre')
        correo = data.get('correo')
        if Usuario.objects(usuario=usuario).first():
            flash('El nombre de usuario ya está registrado', 'error')
            return redirect(url_for('register'))
        if Usuario.objects(correo=correo).first():
            flash('El correo ya está registrado', 'error')
            return redirect(url_for('register'))
        nuevo_usuario = Usuario(
            usuario=usuario,
            password=generate_password_hash(password),
            nombre=nombre,
            correo=correo
        )
        nuevo_usuario.save()
        flash('¡Usuario registrado exitosamente!', 'success')
        correo_destino = nuevo_usuario.correo
        asunto = "Bienvenido al sistema"
        mensaje ="Cuenta creada exitosamente"
        enviar_correo_asincrono(correo_destino, asunto, mensaje)
        return redirect(url_for('login'))  
    return render_template('registrar.html')
