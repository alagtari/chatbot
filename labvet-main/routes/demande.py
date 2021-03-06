from fastapi import Depends,APIRouter,Request
from sqlalchemy.orm import Session
import crud.demande as demande, schemas ,tokens
from database import  SessionLocal


router = APIRouter(tags=['nature'])

db = Session()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

@router.get("/demandes/all")
def get_demandes( request : Request ,db: Session = Depends(get_db)):
    token = request.headers.get('Authorization')
    if (tokens.verify_token(token)):
        demandes = demande.get_demandes(db)
        return {"status" :  200 , "data" : demandes }
    else:
        return{"status" : 403 , "message" :  "token expired."}
    



@router.post("/demandes/create")
async def create_demande(d:schemas.Demande ,request : Request , db: Session = Depends(get_db)):
    
    token = request.headers.get('Authorization')
    if (tokens.verify_token(token)):
        db_demande = demande.get_demande_by_ref(db,d.ref)
        if db_demande:
          return {"status" : 400 , "message" : "demande already exists"}
        demande.create_demande(db,d)
        return   {"status" : 200 , "message": "demande created."}
    else:
        return{"status" : 403,"message" :"token expired"}
    
    




@router.get("/demandes/byid")
def get_demande_by_id(id :int ,request : Request , db: Session = Depends(get_db)):
    token = request.headers.get('Authorization')
    if (tokens.verify_token(token)): 
        db_demande= demande.get_demande_by_ref(db,id)
        if not db_demande:
            return {"status" : 404 , "message" : "demande not found"}    
        return {"status" :  200 , "data" : db_demande }
    else:
        return{"status" : 401 ,"message":"token expired"}
    
@router.get("/demandes/getClientBydemande")
def get_client_by_demande_id(id :int ,request : Request , db: Session = Depends(get_db)):
    token = request.headers.get('Authorization')
    if (tokens.verify_token(token)): 
        db_demande= demande.get_demande_by_ref(db,id)
        if not db_demande:
            return {"status" : 404 , "message" : "demande not found"}    
        return {"status" :  200 , "data" : db_demande.client}
    else:
        return{"status" : 401 ,"message":"token expired"}



@router.get("/demandes/getEchantillonsByDemande")
def get_echantillons_by_demande_id(id :int ,request : Request , db: Session = Depends(get_db)):
    token = request.headers.get('Authorization')
    if (tokens.verify_token(token)): 
        db_demande = demande.get_demande_by_ref(db,id)
        if not db_demande:
            return {"status" : 404 , "message" : "demande not found"}    
        return {"status" :  200 , "data" : db_demande.echantillons }
    else:
        return{"status" : 401 ,"message":"token expired"}
    
@router.delete("/demandes/delete")
def delete_demande(id :int ,request : Request , db: Session = Depends(get_db)):
    token = request.headers.get('Authorization')
    if (tokens.verify_token(token)):  
        if not demande.get_demande_by_ref(db,id):
              return {"status" : 404 , "message" : "demande not found"} 
        demande.delete_demande(db,id)
        return {"status" :  200 , "message" : "demande deleted"}
    else:
        return{"status" : 401 ,"message":"token expired"}
    

