import requests

def test_create_order_real_server():
    url = "http://172.19.15.243:8003/orders/create_order"
    payload = {
        "customer_id": 123,
        "items": [
            { "product_id": 1, "quantity": 2 },
            { "product_id": 2, "quantity": 1 }
        ]
    }

    response = requests.post(url, json=payload)
    assert response.status_code == 201
    print(response.json())
