from redmail import outlook

outlook.username = "pe2ya.flask@hotmail.com"
outlook.password = "flaskText123"

outlook.send(
    receivers=["kalabukhov2004@gmail.com"],
    subject="Ти еблан",
    text="АХАХАХАХАХА <3"
)