from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
# 1,Postman is one of the best tools to test api with bunch of parameters
# 2,It allows you to add key-value pairs for your request parameters and
# it will automatically format your URL:
# 3,t will also allow us to automatically create documentation for your api

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


# with app.create_contact():
#     db.create_all()



    def dict_to(self):
        dictionary={}
    #     loop through each column in the data record
        for column in self.__table__.columns:
    #         create a new diction ary entry
    # where kwy is the name of the column and the value ifs the value of the column
            dictionary[column.name]=getattr(self,column.name)
        return dictionary

# alternatively use dictionary comprehension to do the same thing
#     return {column.name:getattr(self,column.name) for column in self.__table__,columns}
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")


# to basically convert the random_cafe SQLALchemny into json by jsonify
# def get_cafe():
#     pass

# GET IS ALLOWED BY DEFAULT ON ALL ROUTES SO:
@app.route("/random")
def get_cafe():
    result=db.session.execute(db.select(Cafe))
    all_cafes=result.scalars().all()
    random_cafe=random.choice(all_cafes)
    return jsonify(cafe=random_cafe.dict_to())
    # this would be very crazy if we have lot of data so siply convert
    # the random_cafe data record to a dictionary of key-value pairs.
    # return jsonify(cafe={
    #     "id":random_cafe.id,
    #     "name":random_cafe.name,
    #     "map_url":random_cafe.map_url,
    #     "img_url":random_cafe.img_url,
    #     "location":random_cafe.location,
    #     "seats":random_cafe.seats,
    #     "has_toilet":random_cafe.has_toilet,
    #     "has_wifi":random_cafe.has_wifi,
    #     "has_sockets": random_cafe.has_sockets,
    #     "can_take_calls": random_cafe.can_take_calls,
    #     "coffee_price": random_cafe.coffee_price,
    #
    # })

@app.route("/all")
def get_all_cafes():
    result=db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes=result.scalars().all()
    return jsonify(cafes=[cafe.dict_to() for cafe in all_cafes])


@app.route("/search")
def get_cafe_location():
    query_location=request.args.get("loc")
    result=db.session.execute(db.select(Cafe).where(Cafe.location==query_location))
    all_cafes=result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.dict_to() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found":"Sorry we dont have cafe at that location."}),404



@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# updating the price of the cafe

@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    new_price = request.args.get("new_price")
    # to get a cafe y a particular id
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}),200
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}),404

# to delete a cafe
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        cafe = db.get_or_404(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403





## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record



if __name__ == '__main__':
    app.run(debug=True)


# In order to do this, we have to turn our random_cafe SQLAlchemy Object into
# a JSON. This process is called serialization.
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# here is my url for published documentation
# https://documenter.getpostman.com/view/28788998/2s9XxsUbhf


#####################################################