import connexion

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.add_api('swagger.yaml', arguments={'title': 'Data Act Datastore API'})
    # app.debug = True
    app.run(port=80)
