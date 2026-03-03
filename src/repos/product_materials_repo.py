from models.product_materials_model import ProductMaterials
from repos.base_repo import Base


class ProductMaterialsRepo(Base):
    def save(self, record: ProductMaterials):
        sql = """
            INSERT INTO product_materials (nr, pro_code, mat_code, quantity)
            VALUES(?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            conn.execute(
                sql,
                (
                    record.nr,
                    record.pro_code,
                    record.mat_code,
                    record.quantity,
                ),
            )

    def delete(self, record: ProductMaterials):
        sql = """
            DELETE FROM product_materials WHERE nr = ?
        """
        with self.get_connection() as conn:
            conn.execute(sql, (record.nr,))

    def get_all(self) -> dict[str, ProductMaterials]:
        sql = """
            SELECT * FROM product_materials
        """
        record_dict = {}

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            record_list = cursor.fetchall()

        for record in record_list:
            record_dict[str(record[0])] = ProductMaterials(*record)

        return record_dict
