from models.material_model import MaterialRecord, MaterialView
from repos.base_repo import Base


class MaterialRepo(Base):
    def save(self, record: MaterialRecord):
        sql = """
            INSERT INTO materials (code, name, category, base_unit, unit_price, created_at, updated_at)
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
                    float(str(record.unit_price).replace(",", ".")),
                    str(record.created_at),
                    str(record.updated_at),
                ),
            )

    def delete(self, record: MaterialView):
        sql = """
            DELETE FROM materials WHERE code = ?
        """
        with self.get_connection() as conn:
            conn.execute(sql, (record.code,))

    def get_all(self) -> dict[str, MaterialView]:
        sql = """
            SELECT * FROM material_details
        """
        record_dict = {}

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            record_list = cursor.fetchall()

        for record in record_list:
            record_dict[record[0]] = MaterialView(*record)

        return record_dict
