from src.app import App


def main():
  app = App("./cred/serviceAccountKey.json")
  app.start()
  app.generate_csv_file()
  app.generate_xlsx_file()
  # app.saveReservationsByMaterial()


if __name__ == '__main__':
  main()
