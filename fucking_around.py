

# step class
class recipeStep:
    def __init__(self, step_num, step_text):
        self.step_num = step_num
        self.step_text = step_text
        self.ingredients = []
        self.materials = []
    def __str__(self):
        return "Step " + str(self.step_num) + ": " + self.step_text + "\n" + "Step Ingredients: " + str(self.ingredients)