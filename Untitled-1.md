
  employee            projects        assignments
A Restaurant has many Pizzas through RestaurantPizza

  project        employees           assignments
A Pizza has many Restaurants through RestaurantPizza

   assignments                  employee                   project
A RestaurantPizza belongs to a Restaurant and belongs to a Pizza


Update server/models.py to establish the model relationships. Since a RestaurantPizza belongs to a Restaurant and a Pizza, configure the model to cascade deletes.

Set serialization rules to limit the recursion depth.