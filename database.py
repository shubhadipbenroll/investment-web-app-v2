from sqlalchemy import create_engine, text

DB_ENV = 'PROD' #'LOCAL' , 'NP' , 'PROD' , 'UAT'

if DB_ENV == 'LOCAL':
  #Clever-cloud mysql DB connection setup
  engine = create_engine(
      "mysql+pymysql://ugfd2asvp5jsacvp:gdm6RrIc6CrBuFAzTGav@b4ojubqpvk22nbcgfrpe-mysql.services.clever-cloud.com/b4ojubqpvk22nbcgfrpe"
  )

if DB_ENV == 'NP':
  #Local mysql DB connection setup
  engine = create_engine(
      "mysql+pymysql://ugfd2asvp5jsacvp:gdm6RrIc6CrBuFAzTGav@b4ojubqpvk22nbcgfrpe-mysql.services.clever-cloud.com/b4ojubqpvk22nbcgfrpe"
  )

if DB_ENV == 'UAT':
  #Hostgator mysql DB connection setup
  engine = create_engine(
      "mysql+pymysql://omksyite_testinvestmentdb:C5VJ2Ba689pZkjmM@gator4405.hostgator.com/omksyite_testinvestmentdb"
  )

if DB_ENV == 'PROD':
  #Hostgator mysql DB connection setup
  engine = create_engine(
      "mysql+pymysql://omksyite_investmentdb:Em]?j,[dylx+@gator4405.hostgator.com/omksyite_investmentdb"
  )


