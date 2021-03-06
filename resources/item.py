from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    #CLASS VARIABLE NOT OBJECT VARIABLE
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )


    @jwt_required()
    def get(self, name):
        item=ItemModel.find_by_name(name)
        if item is not None:
            return item.json()
        return {"message":"An item with name \'{}\' not found".format(name)}, 404


    def post(self, name):
        if ItemModel.find_by_name(name) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name,**data) # **data =data['price'],data['store_id']

        try:
            item.save_to_db()
        except:
            return {'message':"An error occured while inserting the item"}, 500 #internal server error - 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item=ItemModel(name,**data) # **data =data['price'],data['store_id']
        else:
            item.price=data['price']
            item.store_id=data['store_id']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
        #alternative
        #return {'items':list(map(lambda x: x.json,ItemModel.query.all()))}
