from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://privykurura:Privy%4026119@cluster0.g9tqeky.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tls=True, tlsAllowInvalidCertificates=True)
db = cluster["Mpkcomteck"]
users = db["users"]
orders = db["Orders"]

app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    # number = number.replace("whatsapp:", "")[:-2]
    res = MessagingResponse()
    user = users.find_one({"number": number})
    if bool(user) == False:
        msg = res.message("Hi, thanks for contacting *Mpkcomteck Software development*.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *place* on order \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
        msg.media("https://www.bing.com/images/search?view=detailV2&ccid=udipYlBG&id=2991952EBF42FA33E97AF3D56B4CEB89C510D869&thid=OIP.udipYlBGRLelzij3yjeHLwDIDI&mediaurl=https%3a%2f%2fmedia.licdn.com%2fdms%2fimage%2fD4D16AQEtKwLul491_g%2fprofile-displaybackgroundimage-shrink_200_800%2f0%2f1705565059535%3fe%3d2147483647%26v%3dbeta%26t%3dZ69JD3bP5iJaYIorhEsiI9R4ePB5Xjnt9dFNMrQg284&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.b9d8a962504644b7a5ce28f7ca37872f%3frik%3dadgQxYnrTGvV8w%26pid%3dImgRaw%26r%3d0&exph=200&expw=200&q=mpkcomteck&simid=608041037622173310&FORM=IRPRST&ck=A221AFF3262805B7BC1F2FA606163030&selectedIndex=24&itb=0")
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if option == 1:
            res.message(
                "You can contact us through phone or e-mail.\n\n*Phone*: 0778111517 \n*E-mail* : engineer@mpkcomteck.com")
        elif option == 2:
            res.message("You have entered *ordering mode*.")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
            res.message(
                "You can select one of the following services to order: \n\n1️⃣ Mobile App Develoment  \n2️⃣ Buy my Book \n3️⃣ School Management System"
                "\n4️⃣ AI Bots \n5️⃣ Learn Programming \n6️⃣ Banking System \n7️⃣ Business website \n8️⃣ Portfilio \n9️⃣ E-commerce  \n0️⃣ Go Back")
        elif option == 3:
            res.message("We work from *9 a.m. to 5 p.m*.")

        elif option == 4:
            res.message(
                "We are in Gweru , Zimbabwe. Check our portfolio at *mpkcomteck.com* , or at *mpkcomteck.co.zw*")
        else:
            res.message("Please enter a valid response")
    elif user["status"] == "ordering":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 0:
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            res.message("You can choose from one of the options below: "
                        "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* our software products \n 3️⃣ To know our *working hours* \n 4️⃣ "
                        "To get our *address*")
        elif 1 <= option <= 9:
            cakes = ["Mobile App Develoment", "Buy my Book", "School Management System",
                     "AI Bots ", "Learn Programming", "Banking System", "Business website", "Portfilio", "E-commerce"]
            selected = cakes[option - 1]
            users.update_one(
                {"number": number}, {"$set": {"status": "address"}})
            users.update_one(
                {"number": number}, {"$set": {"item": selected}})
            res.message("Excellent choice 😉")
            res.message("Please enter your location to proceed")
        else:
            res.message("Please enter a valid response")
    elif user["status"] == "address":
        selected = user["item"]
        res.message("Thanks for reaching us 😊")
        res.message(f"Your request for *{selected}* has been received and will respond within an hour")
        orders.insert_one({"number": number, "item": selected, "address": text, "order_time": datetime.now()})
        users.update_one(
            {"number": number}, {"$set": {"status": "ordered"}})
    elif user["status"] == "ordered":
        res.message("Hi, thanks for contacting again.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* software products \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
        users.update_one(
            {"number": number}, {"$set": {"status": "main"}})
    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)


if __name__ == "__main__":
    app.run()
