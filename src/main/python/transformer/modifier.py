class Modifier:
    def __init__(self, function, *new_cols):
        self.function = function
        self.new_cols = new_cols

    def modify(self, string: str) -> str:
        return self.function(string)
