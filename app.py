import csv
import os

def menu(username, products_count):
    # this is a multi-line string, also using preceding `f` for string interpolation
    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Hello, {username}.
    There are {products_count} products in the database.
        operation | description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product.
        'Reset'   | Reset the product list.
    Please select an operation: """ # end of multi- line string. also using string interpolation
    return menu


def read_products_from_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
#    print(f"READING PRODUCTS FROM FILE: '{filepath}'")
    products = []

    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
#            print(row["name"], row["price"])
            products.append(dict(row))


    #TODO: open the file and populate the products list with product dictionaries
    return products

def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
#    print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")
    #TODO: open the file and write a list of dictionaries. each dict should represent a product.

    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "name", "aisle", "department", "price"])
        writer.writeheader() # uses fieldnames set above
        for p in products:
            writer.writerow(p)



def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print("RESETTING DEFAULTS")
    products = read_products_from_file(from_filename)
    write_products_to_file(filename, products)

#def enlarge(i):
#    return i * 100

def auto_inc_id(products):
#adjusted based on s2t2 solution to accomodate zero product ids: https://github.com/prof-rossetti/inventory-mgmt-app-py/commit/fff20b318eaa32c4f4b97322693a5a7c11c06f5a
    if len(products) == 0:
        return 1
    else:
        all_ids = [int(p["id"]) for p in products]
#        max_id = max(all_ids)
#        next_id = max_id + 1
        return max(all_ids) + 1

def run():
    # First, read products from file...
    products = read_products_from_file(filename="products.csv")
    valid = ["list", "show", "create", "update", "destroy"]
    product_count = str(len(products))
    product_list_title = "LISTING "+product_count +" PRODUCTS:"
    product_show_title = "SHOWING A PRODUCT:"
    product_create_title = "CREATING A NEW PRODUCT:"
    product_update_title = "UPDATED A PRODUCT:"
    product_destroy_title = "DESTROYED A PRODUCT:"
    id_error = """

I'm sorry, Dave. I can't do that.

Please try again with a valid product id.

You may enter 'List' to view the full list of available products.

    """


    # Then, prompt the user to select an operation...
    #print(menu(username="@some-user"))
    entry = input(menu(username="Dave", products_count = product_count))
    entry = entry.title() #converting input to title case

    if entry  == "List":
        print("------------------------------")
        print(product_list_title)
        print("------------------------------")
        for pid in products:
            print(" #" + pid["id"] + ": " + pid["name"])

    elif entry == "Show":
        show_entry = input("OK, Dave. Please specify the product identifier:   ")
        valid_entry = False #based on suggestion from : https://stackoverflow.com/questions/3944655/testing-user-input-against-a-list-in-python
        for p in products:
            if show_entry == p["id"]:
                valid_entry = True
        if valid_entry:
            print("------------------------------")
            print(product_show_title)
            print("------------------------------")
            matching_products = [p for p in products if int(show_entry) == int(p["id"])]
            matching_product = matching_products[0]
            print(matching_product)
        else:
            print(id_error)
            run()
#        print(products[int(show_entry)-1])


    #def show_products():

    elif entry == "Create":
        new_product = {
            "id": auto_inc_id(products),
            "name": "New Product",
            "aisle": "New Aisle",
            "department": "New Department",
            "price": 1.00
        }

        create_entry_name = input("OK, Dave. Please enter the name of the new product:   ")
        new_product["name"] = create_entry_name
        create_entry_aisle = input("OK, Dave. Please enter the aisle of the new product:   ")
        new_product["aisle"] = create_entry_aisle
        create_entry_dept = input("OK, Dave. Please enter the department of the new product:   ")
        new_product["department"] = create_entry_dept
        create_entry_price = input("OK, Dave. Please enter the price of the new product:   ")
        new_product["price"] = create_entry_price
        products.append(new_product)

        print("------------------------------")
        print(product_create_title)
        print("------------------------------")
        print(new_product)

    elif entry == "Update":
        update_entry = input("OK, Dave. Please specify the identifier for the product to be updated:   ")
        valid_entry = False
        for p in products:
            if update_entry == p["id"]:
                valid_entry = True
        if valid_entry:
            matching_products = [p for p in products if int(update_entry) == int(p["id"])]
            matching_product = matching_products[0]
            new_name = input("Please enter the new name (current name: " + matching_product["name"] + "):  ")
            matching_product["name"] = new_name
            new_aisle = input("Please enter the new aisle (current aisle: " + matching_product["aisle"] + "):  ")
            matching_product["aisle"] = new_aisle
            new_dept = input("Please enter the new department (current department: " + matching_product["department"] + "):  ")
            matching_product["department"] = new_dept
            new_price = input("Please enter the new price (current price: " + matching_product["price"] + "):  ")
            matching_product["price"] = new_price
            print(product_update_title)
            print(matching_product)
        else:
            print(id_error)
            run()

    elif entry == "Destroy":
        destroy_entry = input("OK, Dave. Please specify the identifier for the product to be destroyed:   ")
        valid_entry = False
        for p in products:
            if destroy_entry == p["id"]:
                valid_entry = True
        if valid_entry:
            matching_products = [p for p in products if int(destroy_entry) == int(p["id"])]
            matching_product = matching_products[0]
            print(product_destroy_title)
            print(matching_product)
            del products[products.index(matching_product)]
        else:
            print(id_error)
            run()

    elif entry == "Reset":
        reset_products_file()

    #elif entry != valid:
    else:
        print("I’m sorry, Dave. I'm afraid I can't do that. Please enter a valid command.")
        run()

    # Then, handle selected operation: "List", "Show", "Create", "Update", "Destroy" or "Reset"...
    #TODO: handle selected operation

    # Finally, save products to file so they persist after script is done...
    write_products_to_file(products=products)



# only prompt the user for input if this script is run from the command-line
# this allows us to import and test this application's component functions
if __name__ == "__main__":
    run()
