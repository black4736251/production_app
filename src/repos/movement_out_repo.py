from models.movement_out_model import MovementOutRecord, MovementOutView
from repos.base_repo import Base


class MovementOutRepo(Base):
    def save(self, record: MovementOutRecord):
        sql = """
            INSERT INTO movements_out (nr, pro_code, cli_code, quantity, created_at, updated_at)
            VALUES(?, ?, ?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            conn.execute(
                sql,
                (
                    record.nr,
                    record.pro_code,
                    record.cli_code,
                    record.quantity,
                    str(record.created_at),
                    str(record.updated_at),
                ),
            )

    def delete(self, record: MovementOutView):
        sql = """
            DELETE FROM movements_out WHERE nr = ?
        """
        with self.get_connection() as conn:
            conn.execute(sql, (record.nr,))

    def get_all(self) -> dict[str, MovementOutView]:
        sql = """
            SELECT * FROM movements_out_details
        """
        record_dict = {}

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            record_list = cursor.fetchall()

        for record in record_list:
            record_dict[record[0]] = MovementOutView(*record)

        return record_dict
