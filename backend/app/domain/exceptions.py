class CustomerException(Exception):
    pass

class CustomerNotFoundException(CustomerException):
    def __init__(self, customer_id):
        super().__init__(f"Customer with id {customer_id} not found.")

class CustomerValidationException(CustomerException):
    def __init__(self, message):
        super().__init__(message)

class CustomerDuplicateException(CustomerException):
    def __init__(self, field, value):
        super().__init__(f"Customer with {field} '{value}' already exists.")
