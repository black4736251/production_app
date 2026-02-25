from models.product_model import ProductRecord, ProductView
from repos.base_repo import Base


class ProductRepo(Base):
    def save(self, record: ProductRecord):
        sql = """
            INSERT INTO products (code, name, category, base_unit, unit_price, created_at, updated_at)
            VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            conn.execute(
                sql,
                (
                    record.code,
                    record.name,
                    record.category.value,
                    record.base_unit.value,
                    float(record.unit_price),
                    str(record.created_at),
                    str(record.updated_at),
                ),
            )

    def delete(self, record: ProductView):
        sql = """
            DELETE FROM products WHERE code = ?
        """
        with self.get_connection() as conn:
            conn.execute(sql, (record.code,))

    def get_all(self) -> dict[str, ProductView]:
        sql = """
            SELECT * FROM product_details
        """
        record_dict = {}

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            record_list = cursor.fetchall()

        for record in record_list:
            record_dict[record[0]] = ProductView(*record)

        return record_dict
