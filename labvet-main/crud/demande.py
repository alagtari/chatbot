
from sqlalchemy.orm import Session
import models, schemas

def get_demande_by_ref(db: Session, ref: int):
    return db.query(models.Demande).filter(models.Demande.ref == ref).first()


def get_demandes(db: Session):
    return db.query(models.Demande).all()

def delete_demande(db: Session, ref: int):
    db_demande =db.query(models.Demande).filter(models.Demande.ref == ref).first()
    db.delete(db_demande)
    db.commit()
    return True

def create_demande(db: Session, demande: schemas.Demande):
    db_demande = models.Demande(ref= demande.ref ,observation=demande.observation,date_reception=demande.date_reception,preleveur=demande.preleveur,controle=demande.controle,client_id=demande.client_id)
    db.add(db_demande)
    db.commit()
    return True

def update_demande(db: Session,demande: schemas.Demande):
    db_demande = get_demande_by_ref(db, demande.ref)
    db_demande.observation = demande.observation
    db_demande.date_reception = demande.date_reception
    db_demande.preleveur  = demande.preleveur
    db_demande.controle = demande.controle
    db_demande.client_id  = demande.client_id
    db.commit()
    return True

def get_client_by_demande(db: Session,ref :int) :
    demande = get_demande_by_ref(db, ref)
    return demande.client


def get_echantillons_by_demande(db: Session,ref :int) :
    demande = get_demande_by_ref(db, ref)
    return demande.echantillons


    
