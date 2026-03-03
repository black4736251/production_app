from models.client_model import Client
from repos.base_repo import Base


class ClientRepo(Base):
    def save(self, record: Client):
        sql = """
            INSERT INTO clients (code, first_name, last_name, cli_type, company_name, country, city, phone, email, date_of_birth, tax_id, created_at, updated_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            conn.execute(
                sql,
                (
                    record.code,
                    record.first_name,
                    record.last_name,
                    record.cli_type,
                    record.company_name,
                    record.country,
                    record.city,
                    record.phone,
                    record.email,
                    str(record.date_of_birth),
                    record.tax_id,
                    str(record.created_at),
                    str(record.updated_at),
                ),
            )

    def delete(self, record: Client):
        sql = """
            DELETE FROM clients WHERE code = ?
        """
        with self.get_connection() as conn:
            conn.execute(sql, (record.code,))

    def get_all(self) -> dict[str, Client]:
        sql = """
            SELECT * FROM clients
        """
        record_dict = {}

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            record_list = cursor.fetchall()

        for record in record_list:
            record_dict[record[0]] = Client(*record)

        return record_dict
