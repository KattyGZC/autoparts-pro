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

class VehicleException(Exception):
    pass

class VehicleNotFoundException(VehicleException):
    def __init__(self, vehicle_id):
        super().__init__(f"Vehicle with id {vehicle_id} not found.")

class VehicleValidationException(VehicleException):
    def __init__(self, message):
        super().__init__(message)

class VehicleDuplicateException(VehicleException):
    def __init__(self, field, value):
        super().__init__(f"Vehicle with {field} '{value}' already exists.")
    
