from typing import List, Dict

import firebase_admin as firebase
import pandas as pd
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import csv
import jsons
from src.models.reservation import Reservation


class App:
  def __init__(self, cred_path: str):
    self._cred = credentials.Certificate(cred_path)
    firebase.initialize_app(self._cred)

    self._client = firestore.client()
    self.reservations = []
    self.reservationByMaterial: Dict[
        str,
        List[firestore.firestore.CollectionReference]
    ] = {}

  @property
  def get_client(self) -> firestore.firestore.Client:
    return self._client

  def get_collection(self, collection) -> firestore.firestore.CollectionReference:
    return self._client.collection(collection)

  def start(self):
    self.reservations = map(
        lambda doc: Reservation(doc),
        self.get_collection("reservation")
        .where("restitue", "==", False)
        .get()
    )

    for res in self.reservations:
      if res.refMateriel not in self.reservationByMaterial:
        self.reservationByMaterial[res.refMateriel] = []
      self.reservationByMaterial[res.refMateriel].append(res)

  def saveReservationsByMaterial(self):
    with open("reservationsByMaterial.json", "w") as f:
      f.write(jsons.dumps(
          {k: [reservation.doc for reservation in self.reservationByMaterial[k]] for k in self.reservationByMaterial}))

  def print_reservation(self):
    for res in self.reservations:
      print(res)

  def admin_return(self, materials: List[str]):
    result = self._client.collection("reservation").where("restitue", "==", False).where(
        "refMateriel", "in", materials).get()

    for res in result:
      self._client.collection("reservation").document(
          res.id).update({"restitue": True})

    print("Number of reservation updated: ", len(result))
    # print(result)

  def generate_csv_file(self):
    with open("exctract.csv", "w", newline="") as f:
      writer = csv.writer(f)
      writer.writerow(
          [
              "material name",
              "should've been returned at",
              "booked by",
              "ref materiel",
              # "status"
          ])

    # now = datetime.now().timestamp()
      now = datetime.utcnow()
      for key, reservations in self.reservationByMaterial.items():
        reservations = [*sorted(reservations, key=lambda x: x.dateFin)]
        reservation = reservations[-1]
        endDate = datetime.fromisoformat(
            reservation.dateFin.__str__()
        ).timestamp()
        endDate = datetime.utcfromtimestamp(endDate)
        if now > endDate:
          writer.writerow([
              reservation.typeMateriel,
              reservation.dateFin,
              reservation.nomValideur,
              reservation.refMateriel,
              # "late"
          ])

  def generate_xlsx_file(self):
    read_file = pd.read_csv("exctract.csv")
    read_file.to_excel("exctract.xlsx", index=None, header=True)
