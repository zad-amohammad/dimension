# dimension
in product.template please create a new char field called dimension

1 - Sale Module
Create a new char field (Dimension:) in the sale order line that reads from product and allows salesperson to add/change the product dimension (e.g 4cm * 12 cm)


2 - Inventory
When confirming sale order system by default create a delivery order to all sortable product, Please create a new char field (Dimension:) in stock.move that read from sale order line also make this field editable (user can edit this field and this will NOT reflect the sale order line)

3 - Invoicing
When create invoice to this sale order please add a new char field (Dimension:) in account invoice line that read from stock move dimension NOT the dimension of sale order line and this field should be readonly
