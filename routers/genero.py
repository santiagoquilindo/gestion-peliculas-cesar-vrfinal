from flask import request,render_template,jsonify,redirect,url_for,session,flash
from models.genero import Genero
from app import app

@app.route("/listgenero/",methods=['GET'])
def listGenero():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    try:
        mensaje=None
        generos=Genero.objects()
    except Exception as error:
        mensaje=str(error)
    return render_template('listadegeneros.html',mensaje=mensaje,generos=generos)
    
@app.route("/agregenero/",methods=['GET', 'POST'])
def addGenero():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    try:
        mensaje=None
        estado=False
        if request.method=='POST':
            datos=request.get_json(force=True)
            genero=Genero(**datos)
            genero.save()
            estado=True
            mensaje="Genero Agregado correctamente"
        else:
            mensaje="No permitido"
    except Exception as error:
        mensaje=str(error)
    return render_template('agregargenero.html',estado=estado,mensaje=mensaje)
        

@app.route("/elimgenero/<id>", methods=['GET'])
def deleteGenero(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    try:
        genero = Genero.objects(id=id).first()
        if genero:
            genero.delete()
        else:
            return redirect(url_for('listGenero'))
    except Exception as e:
        return redirect(url_for('listGenero'))
    return redirect(url_for('listGenero'))


@app.route("/editgenero/<id>", methods=['GET'])
def editGenero(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    genero = Genero.objects(id=id).first()
    if not genero:
        return redirect(url_for('listGenero')) 
    return render_template('editargenero.html', genero=genero)


@app.route("/editgenero/<id>", methods=['POST'])
def updateGenero(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    genero = Genero.objects(id=id).first()
    if not genero:
        return redirect(url_for('listGenero')) 
    nuevo_nombre = request.form.get('nombre')
    if nuevo_nombre:
        genero.update(set__nombre=nuevo_nombre)
        return redirect(url_for('listGenero'))
    return redirect(url_for('listGenero'))
