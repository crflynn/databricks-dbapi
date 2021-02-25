import re
from abc import ABC

from pyhive.sqlalchemy_hive import HiveDialect
from pyhive.sqlalchemy_hive import _type_map
from sqlalchemy import types
from sqlalchemy import util


class DatabricksDialectBase(HiveDialect, ABC):
    def get_table_names(self, connection, schema=None, **kw):
        query = "SHOW TABLES"
        if schema:
            query += " IN " + self.identifier_preparer.quote_identifier(schema)
        return [row[1] for row in connection.execute(query)]

    def get_columns(self, connection, table_name, schema=None, **kw):
        """Get columns according to Databricks' hive or oss hive."""
        rows = self._get_table_columns(connection, table_name, schema)
        # Strip whitespace
        rows = [[col.strip() if col else None for col in row] for row in rows]
        # Filter out empty rows and comment
        rows = [row for row in rows if row[0] and row[0] != "# col_name"]
        result = []
        for (col_name, col_type, _comment) in rows:
            # Handle both oss hive and Databricks' hive partition header, respectively
            if col_name in ("# Partition Information", "# Partitioning"):
                break
            # Take out the more detailed type information
            # e.g. 'map<int,int>' -> 'map'
            #      'decimal(10,1)' -> decimal
            col_type = re.search(r"^\w+", col_type).group(0)
            try:
                coltype = _type_map[col_type]
            except KeyError:
                util.warn("Did not recognize type '%s' of column '%s'" % (col_type, col_name))
                coltype = types.NullType

            result.append(
                {
                    "name": col_name,
                    "type": coltype,
                    "nullable": True,
                    "default": None,
                }
            )
        return result
