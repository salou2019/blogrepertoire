
#Importation de flask
from flask import Flask, render_template, url_for , request , flash , redirect
import psycopg2  
con = psycopg2.connect(user="postgres",
                                  password="salou2019",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="school")
cursor = con.cursor()


#Création de l'application avec la variable app
app = Flask (__name__)
app.secret_key = "message"


@app.route('/')
def index():
    return render_template("projethtml/index.html")

@app.route('/inscription' , methods=['GET', 'POST'])
def inscription():
    cursor.execute("SELECT id_promo, nom_promo FROM promotion")
    apprenant = cursor.fetchall()
    if request.method == "POST":
        flash('Insertion réussit')
        details = request.form
        nom_app = details['nom_ap']
        prenom_app = details['prenom_ap']
        age_app = details['age']
        adresse_app = details['adresse']
        matricule = details['matricule']
        telephone = details['telephone']
        genre = details['genre']
        id_promo = int(details['promo'])
        requete_ajouter_ap="INSERT INTO apprenant(nom , prenom , age , adresse , matricule , telephone , genre , id_promo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(requete_ajouter_ap,(nom_app, prenom_app, age_app, adresse_app , matricule ,telephone , genre ,id_promo))
        con.commit()
    return render_template("projethtml/inscription.html",ap = apprenant)

@app.route('/listepromo' , methods=['GET', 'POST'])
def listepromo():
       #Selection des promos
    cursor.execute("SELECT id_ref, nom_ref FROM referentiel")
    promos = cursor.fetchall()
    if request.method == "POST":
        flash('Insertion réussie')
        details = request.form
        nom_promo = details['nomp']
        date_debut = details['date_debut']
        date_fin = details['date_fin']
        id_ref = int(details['id_ref'])
        requete_ajouter_promo="INSERT INTO promotion(nom_promo,date_debut,date_fin, id_ref) VALUES (%s,%s,%s,%s)"
        cursor.execute(requete_ajouter_promo,(nom_promo, date_debut, date_fin,id_ref))
        con.commit()
    return render_template("projethtml/listepromo.html" ,p = promos)
@app.route('/referentiel' , methods=['GET', 'POST'])
def referentiel():
    if request.method == "POST":
        flash('Insertion réussit')
        details = request.form
        nom_ref = details['nom_ref']
        requete_ajouter_ref="INSERT INTO referentiel(nom_ref) VALUES (%s)"
        cursor.execute(requete_ajouter_ref,(nom_ref,))
        con.commit()

    return render_template("projethtml/referentiel.html")

#Gérer les erreurs avec 404
"""
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
"""



#Exécution de l'application avec run()
if (__name__) == '__main__':
    app.run(debug=True , port=8000)   #acivation du serveur directement pas besoin de redémarrer l'app
