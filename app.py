from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

## import CRUD Operations ##
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

# Create session and connect to DB
engine = create_engine('postgresql://postgres:postgres@localhost:5432/restaurantmenus')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# --------------------------------------------
# Restaurant
# --------------------------------------------

# List Restaurant
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurant/restaurants.html', restaurants=restaurants)

# Create Restaurant
@app.route('/restaurant/new', 
    methods=['GET', 'POST'])
def newRestaurant():
    if(request.method == 'POST'):
        restaurant = Restaurant(name=request.form['name'])
        session.add(restaurant)
        session.commit()
        flash("Restaurant created!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('restaurant/newRestaurant.html')

# Edit Restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', 
    methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if(request.method == 'POST'):
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash("Restaurant updated!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('restaurant/editRestaurant.html', 
            restaurant = restaurant)

# Delete Restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', 
    methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if(request.method == 'POST'):
        session.delete(restaurant)
        session.commit()
        flash("Restaurant deleted!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('restaurant/deleteRestaurant.html', 
            restaurant = restaurant)

# --------------------------------------------
# Menu Item
# --------------------------------------------

# List Menu Item
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id = 
      restaurant_id).all()
    return render_template('menuItem/menu.html', restaurant = restaurant_id, items = items)
    
# Create a Menu Item
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if(request.method == 'POST'):
        newItem = MenuItem(name = request.form['name'], restaurant_id = 
            restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id = 
            restaurant_id))
    else:
        return render_template('menuItem/newmenuitem.html', restaurant_id = 
            restaurant_id)

# Edit Menu
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', 
    methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    myMenuItem = session.query(MenuItem).filter_by(id = menu_id, 
        restaurant_id = restaurant_id).one()
    if(request.method == 'POST'):
        myMenuItem.name = request.form['name']
        session.add(myMenuItem)
        session.commit()
        flash("menu item updated!")
        return redirect(url_for('restaurantMenu', restaurant_id = 
            restaurant_id))
    else:

        return render_template('menuItem/editmenuitem.html', restaurant_id = 
            restaurant_id, menu_id = menu_id, menuItem = myMenuItem)

# Delete Menu Item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', 
    methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id = menu_id, 
        restaurant_id = restaurant_id).one()
    if(request.method == 'POST'):
        session.delete(itemToDelete)
        session.commit()
        flash("menu item deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id = 
            restaurant_id))
    else:

        return render_template('menuItem/deletemenuitem.html', item = itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
