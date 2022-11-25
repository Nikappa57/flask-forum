class Errors:
    def __init__(self, number:int, name:str, desc:str):
        self.number = number
        self.name = name
        self.desc = desc


e404 = Errors(404, 'Not Found', 'Page not found')
e401 = Errors(401, 'Acess Denied', 'Access to this page is denied')
e502 = Errors(502, 'Server Error', 'Internal server error')       