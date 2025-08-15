import requests

def test_create_product_success(product_url, default_headers):
    payload = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 19.99,
        "category": "Food"
        }
        
    res = requests.post(
        f"{product_url}/api/products/",
        json=payload,
        headers=default_headers
    )

    assert res.status_code == 200
    data = res.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]


# ---- Test case 2: Thiếu trường bắt buộc ----
def test_create_product_missing_name(product_url):
    payload = {
        # "name" bị thiếu
        "description": "Sản phẩm lỗi",
        "price": 10000,
        "category": "Lỗi"
    }
    res = requests.post(f"{product_url}/api/products/", json=payload)
    assert res.status_code == 422  # Unprocessable Entity


# ---- Test case 3: Gửi giá âm (logic invalid) ----
def test_create_product_negative_price(product_url):
    payload = {
        "name": "Lỗi giá",
        "description": "Giá âm",
        "price": -10000,
        "category": "Bất hợp lệ"
    }
    res = requests.post(f"{product_url}/api/products/", json=payload)
    assert res.status_code in [400, 422, 500]  # Tùy validation


# ---- Test case 4: Trường rỗng ----
def test_create_product_empty_name(product_url):
    payload = {
        "name": "",
        "description": "Không tên",
        "price": 10000,
        "category": "Ẩn danh"
    }
    res = requests.post(f"{product_url}/api/products/", json=payload)
    assert res.status_code in [400, 422]


# ---- Test case 5: Thiếu toàn bộ dữ liệu ----
def test_create_product_empty_payload(product_url):
    res = requests.post(f"{product_url}/api/products/", json={})
    assert res.status_code == 422



# def test_create_product_with_inventory(mocker, client):
#     # Mock gRPC inventory client trong product service
#     mock_inventory_client = mocker.patch("app.grpc_client.inventory.InventoryStub")
#     mock_check_inventory = mock_inventory_client.return_value.CheckInventory
#     mock_check_inventory.return_value = InventoryReply(available=True)

#     product_data = {
#         "name": "Test Product",
#         "description": "Testing",
#         "price": 100.0,
#         "inventory_id": 1
#     }

#     response = client.post("/products/", json=product_data)
#     assert response.status_code == 200
#     assert response.json()["name"] == "Test Product"
#     mock_check_inventory.assert_called_once()



    