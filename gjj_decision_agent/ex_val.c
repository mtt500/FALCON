#include <stdio.h>
#include <sqlite3.h>

void unsafe_sql_query(sqlite3 *db, const char *username) {
	char query[256];
	snprintf(query, sizeof(query), "SELECT * FROM users WHERE username = '%s'", username);
	
	sqlite3_stmt *stmt;
	int rc = sqlite3_prepare_v2(db, query, -1, &stmt, NULL);
	if (rc != SQLITE_OK) {
		fprintf(stderr, "SQL error: %s\n", sqlite3_errmsg(db));
		return;
	}
	
	while (sqlite3_step(stmt) == SQLITE_ROW) {
		const unsigned char *username = sqlite3_column_text(stmt, 0);
		printf("Username: %s\n", username);
	}
	
	sqlite3_finalize(stmt);
}
