from google.cloud.firestore_v1.document import DocumentSnapshot


class Reservation(DocumentSnapshot):

  def __init__(self, doc: DocumentSnapshot):
    self.dateDebut = doc.get("dateDebut")
    self.dateFin = doc.get("dateFin")
    self.dateReservation = doc.get("dateReservation")
    self.etat = doc.get("etat")
    self.heureReservation = doc.get("heureReservation")
    self.nomValideur = doc.get("nomValideur")
    self.refMateriel = doc.get("refMateriel")
    self.remarque = doc.get("remarque")
    self.restitue = doc.get("restitue")
    self.typeMateriel = doc.get("typeMateriel")
    self.doc = doc
