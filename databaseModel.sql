CREATE TABLE "amount_report" (
	"id"	INTEGER,
	"current_balance"	INTEGER,
	"total_collection"	INTEGER,
	"total_expense"	INTEGER,
	"total_paid"	INTEGER,
	"total_unpaid"	INTEGER,
	"last_updated"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "amount_report" VALUES (1,0,0,0,0,0,0);
CREATE TABLE "expense" (
	"id"	INTEGER,
	"bill_purpose"	TEXT,
	"spent_by"	TEXT,
	"bill_issued_date"	TEXT,
	"bill_image_filename"	TEXT,
	"spent_amount"	INTEGER,
	"remarks"	TEXT,
	"timestamp"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "expense_items" (
	"id"	INTEGER,
	"expense_id"	INTEGER,
	"itemName"	TEXT,
	"itemQty"	TEXT,
	"itemPrice"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "records" (
	"id"	INTEGER,
	"name"	TEXT,
	"amount"	INTEGER,
	"created_at"	INTEGER,
	"status"	TEXT,
	"paid_at"	INTEGER,
	"payment_mode"	TEXT,
	"remarks"	TEXT,
	"is_editable"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);