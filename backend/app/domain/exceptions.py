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
    

class InventoryPartException(Exception):
    pass

class InventoryPartNotFoundException(InventoryPartException):
    def __init__(self, inventory_part_id):
        super().__init__(f"Inventory part with id {inventory_part_id} not found.")

class InventoryPartValidationException(InventoryPartException):
    def __init__(self, message):
        super().__init__(message)

class InventoryPartDuplicateException(InventoryPartException):
    def __init__(self, field, value):
        super().__init__(f"Inventory part with {field} '{value}' already exists.")


class RepairOrderException(Exception):
    pass

class RepairOrderNotFoundException(RepairOrderException):
    def __init__(self, repair_order_id):
        super().__init__(f"Repair order with id {repair_order_id} not found.")

class RepairOrderValidationException(RepairOrderException):
    def __init__(self, message):
        super().__init__(message)

class RepairOrderConflictException(RepairOrderException):
    def __init__(self, message):
        super().__init__(message)


class RepairOrderPartException(Exception):
    pass

class RepairOrderPartNotFoundException(RepairOrderPartException):
    def __init__(self, repair_order_part_id):
        super().__init__(f"Repair order part with id {repair_order_part_id} not found.")

class RepairOrderPartValidationException(RepairOrderPartException):
    def __init__(self, message):
        super().__init__(message)

class RepairOrderPartDuplicateException(RepairOrderPartException):
    def __init__(self, repair_order_id, part_id):
        super().__init__(f"Part with id {part_id} is already associated with repair order {repair_order_id}.")
