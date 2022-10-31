from flaskr import create_app
from .modelos import db, Task
# from flask_mail import Mail

import subprocess

app = create_app('default')
# mail = Mail()

@app.cli.command()
def converter():
    # print('Hello world')
    db.init_app(app)
    # mail.init_app(app)

    tareas = db.session.query(Task).filter_by(state='uploaded')
    # if len(tareas) != 0:
    for tarea in tareas:                
        mypath = tarea.path
#         print("el tipo de variable de mypath es {} y su valor es {}".format(type(mypath),mypath))
        filename = tarea.filename
        newformat = tarea.newformat
        print(mypath + '' + filename + '' + newformat)
#         try:
#             print("Hola tarea con id {}, el path es {} para el archivo {} y con el nuevo formato {} \n".format(tarea.id,mypath,filename,newformat))
            
#             print("vamos a mirar si permite procesar el cambio de audio")                 

#             lista = "ftransc -f " + str(newformat) + " " + str(filename) + " --force-root -w"
#             cmd = ['ftransc', '-f', str(newformat), str(filename), '--force-root','-w']
#             print(lista)
#             subprocess.call(cmd,cwd=mypath)                    
#             print("formato actualizado")
#             tarea.state="procesed"
#             db.session.add(tarea)
#             db.session.commit()
#         except:
#             print("Error con la tarea que tiene id {}".format(tarea.id))
