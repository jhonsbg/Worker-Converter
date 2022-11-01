from flaskr import create_app
from .modelos import db, Task
from datetime import datetime
# from flask_mail import Mail

import subprocess

app = create_app('default')
# mail = Mail()

@app.cli.command()
def converter():
    db.init_app(app)
    # mail.init_app(app)

    tareas = db.session.query(Task).filter_by(state='uploaded')
    # if len(tareas) != 0:
    for tarea in tareas:                
        idUser = tarea.id_usuario
        mypath = "../../audios/" + str(idUser)
        # print("el tipo de variable de mypath es {} y su valor es {}".format(type(mypath),mypath))
        filename = tarea.filename
        newformat = tarea.newformat
        try:
            # print("Hola tarea con id {}, el path es {} para el archivo {} y con el nuevo formato {} \n".format(tarea.id,mypath,filename,newformat))
            # print("vamos a mirar si permite procesar el cambio de audio")                 
            
            print("path donde se actualiza el archivo: " + mypath)                 

            lista = "ftransc -f " + str(newformat) + " " + str(filename) + " --force-root -w"
            cmd = ['ftransc', '-f', str(newformat), str(filename), '--force-root','-w']
            # print(lista)
            tarea.fecha_inicio = datetime.utcnow()
            subprocess.call(cmd,cwd=mypath)                    
            print("formato actualizado")
            tarea.fecha_final = datetime.utcnow()
            tarea.state="procesed"
            db.session.add(tarea)
            db.session.commit()
        except:
            print("Error con la tarea que tiene id {}".format(tarea.id))
