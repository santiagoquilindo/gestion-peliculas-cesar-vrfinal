from flask import render_template,request,url_for,redirect,session
from models.pelicula import Pelicula
from models.genero import Genero
from werkzeug.utils import secure_filename
from flask import jsonify
from app import app
@app.route('/principal')
def index():
    return render_template('index.html')

@app.route("/listpeliculas/",methods=['GET'])
def listPelicula():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    try:
        mensaje=None
        peliculas=Pelicula.objects()
    except Exception as error:
        mensaje=str(error)
        peliculas = []
    return render_template('listadepeliculas.html', mensaje=mensaje, peliculas=peliculas)
    
@app.route("/agrepeliculas/", methods=['GET', 'POST'])
def addPelicula():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    try:
        mensaje = None
        estado = False
        generos = Genero.objects() 
        if request.method == 'POST':
            datos = request.json
            genero_id = datos.get('genero')
            genero = Genero.objects(id=genero_id).first()
            if genero:
                pelicula = Pelicula(
                    codigo=datos.get('codigo'),
                    titulo=datos.get('titulo'),
                    protagonista=datos.get('protagonista'),
                    duracion=datos.get('duracion'),
                    resumen=datos.get('resumen'),
                    foto=datos.get('foto'),
                    genero=genero 
                )
                pelicula.save()
                estado = True
                mensaje = "Película agregada correctamente"
            else:
                mensaje = "Género no encontrado"
        else:
            mensaje = "Método no permitido"
    except Exception as e:
        mensaje = f"Error: {str(e)}"
    return render_template('agregarpelicula.html', estado=estado, mensaje=mensaje, generos=generos)


@app.route("/elimpeliculas/<id>", methods=['GET'])
def deletePelicula(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    try:
        pelicula = Pelicula.objects(id=id).first()
    
        if pelicula:
            pelicula.delete()
        else:
            return redirect(url_for('listPelicula'))
    except Exception as e:
        return redirect(url_for('listPelicula'))
    return redirect(url_for('listPelicula'))


@app.route("/editpeliculas/<id>", methods=['GET'])
def editPelicula(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    pelicula = Pelicula.objects(id=id).first()
    if not pelicula:
        return redirect(url_for('listPelicula'))
    generos = Genero.objects()
    return render_template('editarpelicula.html', pelicula=pelicula,generos=generos)

@app.route("/editpeliculas/<id>", methods=['POST'])
def updatePelicula(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    pelicula = Pelicula.objects(id=id).first()
    if not pelicula:
        return redirect(url_for('listPelicula'))
    nuevocodigo = request.form.get('codigo')
    nuevotitulo = request.form.get('titulo')
    nuevo_protagonista = request.form.get('protagonista')
    nuevo_duracion = request.form.get('duracion')
    nuevo_resumen = request.form.get('resumen')
    nuevo_foto = request.form.get('foto')
    nuevo_genero = request.form.get('genero')
    genero = Genero.objects(id=nuevo_genero).first() if nuevo_genero else None
    if nuevo_genero and not genero:
        return redirect(url_for('listPelicula'))
    pelicula.update(
        set__codigo=nuevocodigo,
        set__titulo=nuevotitulo,
        set__protagonista=nuevo_protagonista,
        set__duracion=nuevo_duracion,
        set__resumen=nuevo_resumen,
        set__foto=nuevo_foto,
        set__genero=genero if genero else pelicula.genero 
    )
    return redirect(url_for('listPelicula'))