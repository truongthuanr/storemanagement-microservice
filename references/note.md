🛒 Flow

Merchant tạo sản phẩm → product-service.create_product()

Merchant nhập hàng → inventory-service.create_stock(product_id, qty)

User xem product → frontend gọi product-service.get_product(product_id) + inventory-service.get_stock(product_id)

User đặt hàng → order-service.reserve_stock() gọi inventory