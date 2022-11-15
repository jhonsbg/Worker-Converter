from flaskr import create_app
from flask import request
from .modelos import db, Task
from datetime import datetime
# from flask_mail import Mail

# Import Google Client Libraries
from google.cloud import storage

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
        mypath = str(idUser) + "/"
        # print("el tipo de variable de mypath es {} y su valor es {}".format(type(mypath),mypath))
        filename = tarea.filename
        newformat = tarea.newformat
        try:
            # print("Hola tarea con id {}, el path es {} para el archivo {} y con el nuevo formato {} \n".format(tarea.id,mypath,filename,newformat))
            # print("vamos a mirar si permite procesar el cambio de audio")                 
            
            # print("path donde se actualiza el archivo: " + mypath)                 

            # lista = "ftransc -f " + str(newformat) + " " + str(filename) + " --force-root -w"

            # Dowload file from GCP Bucket
            bucket_name = "audio_storage_cloud"
            source_blob_name = filename
            destination_file_name = filename
            
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_name)

            print(
                "Downloaded storage object {} from bucket {} to local file {}.".format(
                    source_blob_name, bucket_name, destination_file_name
                )
            )

            cmd = ['ftransc', '-f', str(newformat), str(filename), '--force-root','-w']
            # print(lista)
            tarea.fecha_inicio = datetime.utcnow()
            subprocess.call(cmd,cwd=mypath)                    
            print("formato actualizado")

            # Save the file in Bucket of GCP
            bucket_name = "audio_storage_cloud"
            destination_blob_name = mypath + filename
            name_file = tarea.filename[:-3]
            new_name_file = name_file + tarea.newformat
            contents = new_name_file

            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)

            blob.upload_from_file(request.files["file"], content_type='audio/mpeg')

            print(
                f"{destination_blob_name} with contents {contents} uploaded to {bucket_name}."
            )

            # Update task information in DB
            tarea.fecha_final = datetime.utcnow()
            tarea.state="procesed"
            db.session.add(tarea)
            db.session.commit()
        except:
            print("Error con la tarea que tiene id {}".format(tarea.id))
