from flask import Flask, render_template, request, redirect





class Promo(object):
    """__init__() functions as the class constructor"""
    def __init__(self, id, nom, dateDebut, dateFin):
        self.id = id
        self.dateDebut = dateDebut
        self.dateFin = dateFin
        self.nom = nom

listePromo = []
listePromo.append(Promo(1, 'P2016', '2016', '2017'))
listePromo.append(Promo(2, 'P2017', '2017', '2018'))
listePromo.append(Promo(3, 'P2018', '2018', '2019'))
listePromo.append(Promo(4, 'P2019', '2020', '2020'))

