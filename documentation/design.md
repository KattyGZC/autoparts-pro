# Major Design Decisions and Trade-offs overview

## Architecture
For this challenge, I have chosen to use a monolithic architecture with Clean Architecture principles, but keeping a decoupled structure between frontend and backend, orchestrating all with Docker. This decision was made to focus on the core functionality of the system and to keep the codebase simple and easy to maintain. 

## Database Design
The safer and standard way is design a normalized relational schema. It will use PostgreSQL as the database. In this case we have to design a database schema that efficiently supports core business processes, minimizes stock shortages and waste, optimizes repair order processing, keeps scalable and maintainable as the system grows.  It will have five tables: Customer, Vehicle, InventoryParts, RepairOrder and RepairOrderPart. The last one is a junction table for the many-to-many relationship between RepairOrder and InventoryParts.

1. **Customer**: id, name, email, phone 

Central entity to link with Vehicle and RepairOrder. Keeping customer data separated from vehicle data to avoid data duplication.

2. **Vehicle**: id, customer_id, model, year, license_plate, color

Vehicles are serviced assets, tightly coupled repair orders. 

3. **InventoryParts**: id, code, description, cost, stock

Central to the inventory system, every repair order will use parts from the inventory. Tracking stock directly in this table keeps inventory management simple and efficient.

4. **RepairOrder**: id, customer_id, vehicle_id, date, status, labor

Represents each repair task, linking to Customer, Vehicle and parts. Storing vehicle and customer references allows quick association.

5. **RepairOrderPart**: id, repair_order_id, inventory_part_id, quantity, unit_cost

Many-to-many relationship between repair orders and parts used in them. It enables tracking of parts used in each repair order and decouples part usage from inventory tracking. Besides, it supports optimization logic: given current inventory, which repair order can be fulfilled

### Normalization Approach
The database schema is normalized to third normal form (3NF), which means that it is free of any transitive dependencies and there are no partial dependencies. This ensures data integrity and reduces the risk of data anomalies.
- Ensure that all attributes are atomic and independent of each other.
- Remove partial dependencies between attributes.
- Remove transitive dependencies.

### Trade-offs
- Storing stock directly in InventoryPart is simple and performant, but it can lead to data consistency issues if not properly managed. 
- Avoiding embedded structures ensure relational integrity and simplify reporting and analytics.
- Slightly more JOINs in queries, but it's a small price to pay for the benefits of a normalized schema, JOINs are optimized in PostgreSQL.

### Limitations
1. **Stock trakings lacks audit trail**: The "stock" field in "InventoryParts" is efficient but doesn't provide a history of stock changes, making it challenging to track inventory issues of perform audits.
2. **Scalability for multi-branch operations**: The current design assumes a single store. Supporting multiple stores would require refactoring and adding location-based inventory control.
3. **Lack of historical pricing and cost tracking**: Only the current cost is stored per part. There is no mechanism to track cost changes and variations over time, which limits accurate profitability and historical analysis.
