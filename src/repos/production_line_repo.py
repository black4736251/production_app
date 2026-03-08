from models.production_line_model import ProductionLineRecord, ProductionLineView
from repos.base_repo import Base


class ProductionLineRepo(Base):
    def save(self, record: ProductionLineRecord):
        sql = """
            INSERT INTO production_line (nr, pro_code, quantity, created_at, updated_at)
            VALUES(?, ?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            conn.execute(
                sql,
                (
                    record.nr,
                    record.pro_code,
                    record.quantity,
                    str(record.created_at),
                    str(record.updated_at),
                ),
            )

    def delete(self, record: ProductionLineView):
        sql = """
            DELETE FROM production_line WHERE nr = ?
        """
        with self.get_connection() as conn:
            conn.execute(sql, (record.nr,))

    def get_all(self) -> dict[str, ProductionLineView]:
        sql = """
            SELECT * FROM production_line_details
        """
        record_dict = {}

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            record_list = cursor.fetchall()

        for record in record_list:
            record_dict[str(record[0])] = ProductionLineView(*record)

        return record_dict
