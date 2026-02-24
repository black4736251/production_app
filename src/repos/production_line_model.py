from models.movement_in_model import MovementInRecord, MovementInView
from models.production_line_model import ProductionLineRecord
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

    def delete(self, record: MovementInRecord):
        sql = """
            DELETE FROM production_line WHERE nr = ?
        """
        with self.get_connection() as conn:
            conn.execute(sql, (record.nr,))

    def get_all(self) -> dict[str, MovementInView]:
        sql = """
            SELECT * FROM production_line
        """
        record_dict = {}

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            record_list = cursor.fetchall()

        for record in record_list:
            record_dict[record[0]] = MovementInView(*record)

        return record_dict
