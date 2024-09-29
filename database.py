from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://ugfd2asvp5jsacvp:gdm6RrIc6CrBuFAzTGav@b4ojubqpvk22nbcgfrpe-mysql.services.clever-cloud.com/b4ojubqpvk22nbcgfrpe"
)

"""with engine.connect() as conn:
  result = conn.execute(text("select * from Users"))

  #print("type(result.all())", type(result.all()))
  print(result.all())

  result_dicts = []

  for row in result.all():
    result_dicts.append(row)

  print("result_dicts", result_dicts)
"""
