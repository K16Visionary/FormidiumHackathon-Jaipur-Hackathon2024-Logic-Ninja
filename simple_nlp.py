import re

class SimpleNLP:
    def __init__(self, table_name="accounts"):
        self.table_name = table_name
        self.column_mapping = {
            "id": "id",
            "identifier": "id",
            "account id": "id",
            "name": "name",
            "account name": "name",
            "account_type": "account_type",
            "type": "account_type",
            "balance": "balance",
        }

    def generate_sql_query(self, query, keywords, table_name="accounts"):
        query = query.lower()
        words = re.findall(r'\b\w+\b', query)
        columns = [self.column_mapping.get(word) for word in words if word in self.column_mapping]
        operators = [word for word in words if word in ['=', '>', '<', '>=', '<=', '!=']]
        values = [word.strip("'") for word in words if word.startswith("'") and word.endswith("'")]
        aggregate_functions = [word for word in words if word in ['average', 'avg', 'highest', 'lowest', 'sum', 'count', 'maximum']]

        # Pre-defined static messages
        static_messages = {
            "show maximum balance": "SELECT MAX(balance) AS 'Maximum Balance' FROM accounts",
            "show maximum": "SELECT MAX(*) FROM accounts",
            "show all": "SELECT * FROM accounts",
            "show highest balance": "SELECT * FROM accounts ORDER BY balance DESC LIMIT 1",
            "show lowest balance": "SELECT * FROM accounts ORDER BY balance ASC LIMIT 1",
            "show average balance": "SELECT AVG(balance) AS 'Average Balance' FROM accounts",
              # Show all accounts
            "show all accounts": "SELECT * FROM accounts",
            "list all accounts": "SELECT * FROM accounts",
            # Show specific columns
            "show all names": "SELECT name FROM accounts",
            "show all balances": "SELECT balance FROM accounts",
            "list all account types": "SELECT account_type FROM accounts",
            "name, balance": "SELECT name, balance FROM accounts",
            # Filter by Column Values
            # Direct comparison
            "account_type = 'savings'": "SELECT * FROM accounts WHERE account_type = 'savings'",
            "balance > 10000": "SELECT * FROM accounts WHERE balance > 10000",
            "name = 'John Doe'": "SELECT * FROM accounts WHERE name = 'John Doe'",
            # Name starts with
            "name starts with 'A'": "SELECT * FROM accounts WHERE name LIKE 'A%'",
            "accounts whose name starts with 'S'": "SELECT * FROM accounts WHERE name LIKE 'S%'",
            # Comparisons using operators
            "balance > 5000": "SELECT * FROM accounts WHERE balance > 5000",
            "balance <= 2000": "SELECT * FROM accounts WHERE balance <= 2000",
            "account_type != 'checking'": "SELECT * FROM accounts WHERE account_type != 'checking'",
            # Combined Filters
            "account_type = 'checking' AND balance > 1000": "SELECT * FROM accounts WHERE account_type = 'checking' AND balance > 1000",
            "name starts with 'M' AND balance < 3000": "SELECT * FROM accounts WHERE name LIKE 'M%' AND balance < 3000",
            # Add more static messages as needed
        }

        if query in static_messages:
            return static_messages[query]

        # Your existing logic for dynamic queries
        select_clause = "SELECT "
        if aggregate_functions:
            if aggregate_functions[0] in ['highest', 'lowest', 'maximum']:
                select_clause += "*"
            elif aggregate_functions[0] == 'count':
                select_clause += f"COUNT({columns[0] if columns else '*'})"
            else:
                select_clause += f"{aggregate_functions[0]}({columns[0] if columns else 'balance'}) AS '{aggregate_functions[0].capitalize()} Balance'"
        else:
            select_clause += ", ".join(columns) if columns else "*"

        from_clause = f"FROM {self.table_name}"
        where_clause = ""
        order_by_clause = ""
        limit_clause = ""

        # Your existing logic for building WHERE, ORDER BY, and LIMIT clauses

        where_clause = where_clause[:-5] if where_clause else ""  # Remove trailing " AND "

        sql_query = f"{select_clause} {from_clause} {f'WHERE {where_clause}' if where_clause else ''} {order_by_clause} {limit_clause}"
        print(sql_query)  # For debugging
        return sql_query

# Usage example
nlp = SimpleNLP()
query = "show highest balance"
sql_query = nlp.generate_sql_query(query, [])
print(sql_query)
