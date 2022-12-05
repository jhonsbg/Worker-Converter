from flask import request
from datetime import datetime
from flaskr import create_app
from .modelos import db, Task

from concurrent.futures import TimeoutError
import subprocess

# Google Cloud Services
from google.cloud import storage
from google.cloud import pubsub_v1

app = create_app('default')

# @app.cli.command()
@app.route('/')
def converter():
    db.init_app(app)

    timeout = 5.0 

    # Subscriber Google Pub/Sub configuration
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = 'projects/cloud-andes-conversion-tool/subscriptions/Prueba-Audio-sub'

    def callback(message):
        print(f'Received message: {message}')
        print(f'data: {message.data}')

        if message.attributes:
            print("Attributes:")
            for key in message.attributes:
                value = message.attributes.get(key)
                print(f"{key}: {value}")

            audioConverter(message.attributes["id"], message.attributes["filename"], message.attributes["newformat"])

        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f'Listening for messages on {subscription_path}')

    def audioConverter(idUser, fileName, newFormat):
            # Declare variables
            idUser = idUser
            filename = fileName
            newformat = newFormat

            mypath = str(idUser) + "/"
            completePath = mypath + filename
            name_file = filename[:-3]
            new_name_file = name_file + newformat
            newPathFile = mypath + new_name_file


            try:            
                # Dowload file from GCP Bucket
                bucket_name = "audio_storage_cloud"
                source_blob_name = completePath
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
                
                # Audio convert
                cmd = ['ftransc', '-f', str(newformat), str(filename), '--force-root','-w']
                # fecha_inicio = datetime.utcnow()
                subprocess.call(cmd)        
                print("Formato actualizado")

                # Save the file in Bucket of GCP
                bucket_name = "audio_storage_cloud"
                destination_blob_name = newPathFile
                contents = new_name_file

                storage_client = storage.Client()
                bucket = storage_client.bucket(bucket_name)
                blob = bucket.blob(destination_blob_name)

                blob.upload_from_filename("./" + new_name_file, content_type='audio/mpeg')

                print(
                    f"{destination_blob_name} with contents {contents} uploaded to {bucket_name}."
                )

                # Update task information in DB
                #tarea.fecha_final = datetime.utcnow()
                #tarea.state="procesed"
                #db.session.add(tarea)
                #db.session.commit()
            except:
                print("Error con la tarea que tiene id")


    with subscriber:                                                # wrap subscriber in a 'with' block to automatically call close() when done
        try:
            # streaming_pull_future.result(timeout=timeout)
            streaming_pull_future.result()                          # going without a timeout will wait & block indefinitely
        except TimeoutError:
            streaming_pull_future.cancel()                          # trigger the shutdown
            streaming_pull_future.result()   


    # Database Query
    #tareas = db.session.query(Task).filter_by(state='uploaded')

