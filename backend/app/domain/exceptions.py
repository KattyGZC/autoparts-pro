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
    def __init__(self, part_name, repair_order_id):
        super().__init__(f"Part with name {part_name} is already associated with repair order {repair_order_id}.")


class RepairOrderOptimizationException(Exception):
    pass


class NoAvailableRepairOrdersException(RepairOrderOptimizationException):
    def __init__(self):
        super().__init__("No available repair orders to optimize.")


class InventoryConstraintException(RepairOrderOptimizationException):
    def __init__(self, part_id: str):
        super().__init__(f"Not enough inventory for part with ID: {part_id} to fulfill any repair order.")


class InvalidRepairOrderDataException(RepairOrderOptimizationException):
    def __init__(self, repair_order_id: str, reason: str):
        super().__init__(f"Repair order '{repair_order_id}' has invalid data: {reason}")


class OptimizationAlgorithmException(RepairOrderOptimizationException):
    def __init__(self, message: str = "Unexpected error occurred during optimization process."):
        super().__init__(message)
