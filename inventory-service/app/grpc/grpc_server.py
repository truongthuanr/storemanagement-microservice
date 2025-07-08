# app/grpc/grpc_server.py
import grpc, asyncio
from concurrent.futures import ThreadPoolExecutor

from app.proto import inventory_pb2, inventory_pb2_grpc
from app.database import SessionLocal
from app.services import inventory_service as svc
from app.mappers.inventory_mapper import to_proto_item
from servicelogging.servicelogger import logger


class InventoryServiceImpl(inventory_pb2_grpc.InventoryServiceServicer):

    # ---------- List -------------------------------------------------
    async def ListInventory(self, request, context):
        db = SessionLocal()
        try:
            data = svc.list_inventory(db)
            resp = inventory_pb2.InventoryListResponse(
                inventories=[inventory_pb2.InventoryResponse(**d) for d in data]
            )
            return resp
        finally:
            db.close()

    # ---------- Get --------------------------------------------------
    async def GetInventory(self, request, context):
        db = SessionLocal()
        try:
            d = svc.get_inventory(db, request.id)
            if not d:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return inventory_pb2.InventoryResponse()
            return inventory_pb2.InventoryResponse(**d)
        finally:
            db.close()

    # ---------- Create ----------------------------------------------
    async def CreateInventory(self, request, context):
        logger.info("CreateInventory Started")
        db = SessionLocal()
        try:
            d = svc.create_inventory(
                db,
                product_id=request.product_id, 
                name=request.name,
                description=request.description,
                price=request.price,
                stock=request.stock,
            )
            item = to_proto_item(d)
            logger.info(
                    f"CreateInventory return | "
                    f"item ={item}"
    )
            return inventory_pb2.InventoryResponse(item=item)
        finally:
            db.close()


    # ---------- Update ----------------------------------------------
    async def UpdateInventory(self, request, context):
        db = SessionLocal()
        try:
            d = svc.update_inventory(
                db,
                request.id,
                name=request.name,
                description=request.description,
                price=request.price,
                stock=request.stock,
            )
            if not d:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return inventory_pb2.InventoryResponse()
            return inventory_pb2.InventoryResponse(**d)
        finally:
            db.close()

    # ---------- Delete ----------------------------------------------
    async def DeleteInventory(self, request, context):
        db = SessionLocal()
        try:
            ok = svc.delete_inventory(db, request.id)
            return inventory_pb2.DeleteInventoryResponse(success=ok)
        finally:
            db.close()

    # ---------- Reserve stock (used by Order) ------------------------
    async def ReserveStock(self, request, context):
        db = SessionLocal()
        items = [{"id": i.id, "quantity": i.quantity} for i in request.items]
        try:
            ok = svc.reserve_stock(db, items)
            return inventory_pb2.ReserveStockResponse(success=ok)
        finally:
            db.close()


# ---------- Server bootstrap ----------------------------------------
async def serve_grpc():
    server = grpc.aio.server(ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryServiceImpl(), server)
    addr = "[::]:50051"
    server.add_insecure_port(addr)
    print(f"[gRPC] Inventory Service is running on {addr}")
    await server.start()
    await server.wait_for_termination()
