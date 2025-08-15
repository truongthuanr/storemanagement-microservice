import requests

# ------- Testcase 1: Get stock by product id ----------------------------------
# Product service call inventory service by gRPC to get stock by product_id    #
def test_read_inventory_grpc(product_url):
    product_id = 1  # 

    response = requests.get(f"{product_url}/api/products/{product_id}/inventory")

    assert response.status_code == 200
    json_data = response.json()
    assert "product_id" in json_data
    assert json_data["product_id"] == product_id
    assert "total_stock" in json_data
    assert isinstance(json_data["total_stock"], int)