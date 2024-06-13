-- creates a trigger that decreases the quantity of an item after adding a new order.
-- This is a trigger that is called after an insert operation on the order table.
-- It decreases the quantity of the item in the item table by the quantity ordered.
-- Quantity in the table items can be negative.
DELIMITER $$

CREATE TRIGGER decrease_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
	UPDATE items
	SET quantity = quantity - NEW.number
	WHERE name = new.item_name;
END $$

DELIMITER ;
