from models.movement_in_model import MovementInRecord, MovementInView
from repos.base_repo import Base


class MovementInRepo(Base):
    def save(self, record: MovementInRecord):
        sql = """
            INSERT INTO movements_in (nr, mat_code, sup_code, quantity, created_at, updated_at)
            VALUES(?, ?, ?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            conn.execute(
                sql,
                (
                    record.nr,
                    record.mat_code,
                    record.sup_code,
                    record.quantity,
                    str(record.created_at),
                    str(record.updated_at),
                ),
            )

    def delete(self, record: MovementInRecord):
        sql = """
            DELETE FROM movements_in WHERE nr = ?
        """
        with self.get_connection() as conn:
            conn.execute(sql, (record.nr,))

    def get_all(self) -> dict[str, MovementInView]:
        sql = """
            SELECT * FROM movements_in_details
        """
        record_dict = {}

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            record_list = cursor.fetchall()

        for record in record_list:
            record_dict[record[0]] = MovementInView(*record)

        return record_dict
