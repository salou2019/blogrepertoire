from flask import Flask , render_template,url_for, redirect, request, flash
import psycopg2 as psy

app = Flask(__name__)
def conndb():
    try:
        connection = psy.connect(user="postgres",
                                host="localhost",
                                port="5432",
                                password="yakhouya",
                                database="projet_2"
                               )
        return connection
    except(Exception) as error :
        print ("Il ya un probleme de connection  a la base de donne" ,error)
conn = conndb()
curseur = conn.cursor()

app = Flask(__name__)

app.secret_key = "message"

###Pour l'aceuil
@app.route('/')
def nav():
    return render_template('nav.html')




# ### Pour le fichier inscription
# @app.route('/form_inscription.html')
# def form_inscription():
#     return render_template('form_inscription.html')




# ##################
# @app.route('/form_modification.html')
# def form_modification():
#     return render_template('form_modification.html')


@app.route('/nouveau_ref')
def nouveau_ref():
    return render_template('nouveau_ref.html')



### Pour l'insertion de referentiel
@app.route('/nouveau_ref', methods = ['POST'])
def nouveauref():
    nom_ref = request.form['nom_ref']
    curseur.execute("INSERT INTO referentiel (nom_ref) VALUES (%s)", (nom_ref,))
    conn.commit()

    return redirect(url_for('nouveau_ref'))
### Fin de l'ajout de referentiel


### Pour l'ajout de promo
@app.route('/ajout_promo', methods = ['POST','GET'])
def ajout_promo():
    conn = conndb()
    curseur = conn.cursor()
    curseur.execute("SELECT * FROM referentiel")
    data=curseur.fetchall()
    # curseur.close()
    if request.method =='POST':
        nom_promo = request.form['nom_promo']
        debut = request.form['debut']
        fin = request.form['fin']
        nom_ref = request.form['ref']
        curseur.execute("INSERT INTO promo (nom_promo, date_debut, date_fin, id_ref ) VALUES (%s, %s, %s, %s)", (nom_promo, debut, fin, nom_ref))
        conn.commit()
    return render_template('ajout_promo.html', ref=data)
    # return redirect(url_for('ajout_promo'))
### Fin de l'ajout pour promo


### Pour l'inscription d'un apprenant
 
 

@app.route('/inscription', methods = ['POST','GET'])
def inscription():
    curseur.execute("SELECT * FROM promo")
    i=curseur.fetchall()
    conn.commit
    if request.method =='POST':
        prenom = request.form['prenom']
        nom = request.form['nom']
        datenais = request.form['datenais']
        numero = request.form['numero_tel']
        matricule = request.form['matricule']
        email = request.form['email']
        adresse = request.form['adresse']
        nom_promo= request.form['promo']
       
        curseur.execute("INSERT INTO apprenant (prenom, nom, date_de_naissence, numero_tel, e_mail, adress, id_promo, matricule ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(prenom, nom, datenais, numero, email, adresse, nom_promo, matricule))
        conn.commit()
        
        
    return render_template('form_inscription.html', promo=i)


#############################################################################################
#############################################################################################

###Pour la Modification 

### Modification de referentiel

@app.route('/modif_ref')
def modif_ref():
    conn = conndb()
    curseur = conn.cursor()
    curseur.execute("SELECT * FROM referentiel")
    data1=curseur.fetchall()

    return render_template('modifier_ref.html', ref=data1 )

@app.route('/modif_ref',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        ref = request.form['id']
        nom = request.form['nom_ref']        
        curseur.execute("UPDATE referentiel SET nom_ref=%s WHERE id_ref=%s", (nom,ref))
        flash("Data Updated Successfully")
        conn.commit()
        return redirect(url_for('modif_ref'))

### Modification de la promotion

@app.route('/modif_promo')
def modif_promo():
    conn = conndb()
    curseur = conn.cursor()
    curseur.execute("SELECT * FROM promo")
    data2=curseur.fetchall()

    conn = conndb()
    curseur = conn.cursor()
    curseur.execute("SELECT * FROM referentiel")
    data3=curseur.fetchall()

    return render_template('modifier_promo.html', pro=data2, refe=data3 )

@app.route('/modif_promo',methods=['POST','GET'])
def update_promo():

    if request.method == 'POST':
        id_promo = request.form['id']
        nom = request.form['nom_promo']
        debut = request.form['date_debut']
        fin = request.form['date_fin']
        nom_ref = request.form['nom_ref']        
        curseur.execute("UPDATE promo SET nom_promo=%s, date_debut=%s, date_fin=%s, id_ref=%s  WHERE id_promo=%s", ( nom, debut, fin, nom_ref, id_promo))
        flash("Data Updated Successfully")
        conn.commit()
        return redirect(url_for('modif_promo'))


### Modification de l'apprenant


### Modification de l'apprenant

@app.route('/modif_apprenant')
def modif_apprenant():
    conn = conndb()
    curseur = conn.cursor()
    curseur.execute("SELECT apprenant.id_apprenant, apprenant.matricule, apprenant.prenom, apprenant.nom, apprenant.date_de_naissence, apprenant.numero_tel, apprenant.e_mail, apprenant.adress, promo.nom_promo FROM apprenant, promo WHERE apprenant.id_promo=promo.id_promo")
    data4=curseur.fetchall()

    conn = conndb()
    curseur = conn.cursor()
    curseur.execute("SELECT * FROM referentiel")
    data5=curseur.fetchall()

    return render_template('form_modification.html', pro=data4, refe=data5 )

@app.route('/modif_apprenant',methods=['POST','GET'])
def update_apprenant():

    if request.method == 'POST':
        id_apprenant = request.form['id']
        prenom = request.form['prenom']
        nom = request.form['nom']
        date_n = request.form['date_de_naissence']
        numero = request.form['numero_tel']
        mail = request.form['e_mail']
        nom_promo = request.form['nom_promo']
        matricule = request.form['matricule']
        curseur.execute("UPDATE apprenant SET prenom=%s, nom=%s, date_de_naissence=%s, numero_tel=%s, e_mail=%s, nom_promo=%s, matricule=%s WHERE id_apprenant=%s", (prenom, nom, date_n, numero, mail, nom_promo, matricule, id_apprenant))
        flash("Data Updated Successfully")
        conn.commit()
        return redirect(url_for('modif_apprenant'))



if __name__ == '__main__':  

    app.run(debug=True, port=3000)