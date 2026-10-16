-- StudentBridge AI / MySQL 8.0 schema. Research AND sandbox tables.
CREATE DATABASE IF NOT EXISTS studentbridge_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE studentbridge_ai;
SET NAMES utf8mb4;


CREATE TABLE IF NOT EXISTS audit (
	id BIGINT NOT NULL AUTO_INCREMENT, 
	occurred_at VARCHAR(40) NOT NULL, 
	event_type VARCHAR(90) NOT NULL, 
	object_id VARCHAR(80) NOT NULL, 
	event_json TEXT NOT NULL, 
	previous_hash VARCHAR(64) NOT NULL, 
	event_hash VARCHAR(64) NOT NULL, 
	PRIMARY KEY (id)
)ENGINE=InnoDB

;


CREATE TABLE IF NOT EXISTS audit_chain_state (
	state_id INTEGER NOT NULL AUTO_INCREMENT, 
	last_hash VARCHAR(64) NOT NULL, 
	PRIMARY KEY (state_id)
)ENGINE=InnoDB

;


CREATE TABLE IF NOT EXISTS provider_events (
  event_id VARCHAR(120) NOT NULL,
  session_id VARCHAR(150) NOT NULL,
  event_type VARCHAR(100) NOT NULL,
  payment_status VARCHAR(30) NOT NULL,
  received_at VARCHAR(40) NOT NULL,
  PRIMARY KEY (event_id)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS countries (
	country_code VARCHAR(2) NOT NULL, 
	country_name VARCHAR(100) NOT NULL, 
	currency_code VARCHAR(3), 
	currency_name VARCHAR(100), 
	data_status VARCHAR(60) NOT NULL, 
	notes TEXT, 
	PRIMARY KEY (country_code)
)ENGINE=InnoDB

;


CREATE TABLE IF NOT EXISTS plans (
	id VARCHAR(40) NOT NULL, 
	created_at VARCHAR(40) NOT NULL, 
	payload_json TEXT NOT NULL, 
	result_json TEXT NOT NULL, 
	decision_hash VARCHAR(64) NOT NULL, 
	PRIMARY KEY (id)
)ENGINE=InnoDB

;


CREATE TABLE IF NOT EXISTS sources (
	source_id INTEGER NOT NULL AUTO_INCREMENT, 
	publisher VARCHAR(255) NOT NULL, 
	title VARCHAR(500) NOT NULL, 
	source_url TEXT NOT NULL, 
	source_type VARCHAR(100) NOT NULL, 
	published_or_updated_date VARCHAR(100), 
	collection_date VARCHAR(30) NOT NULL, 
	notes TEXT, 
	PRIMARY KEY (source_id)
)ENGINE=InnoDB

;


CREATE TABLE IF NOT EXISTS financial_benchmarks (
	benchmark_id INTEGER NOT NULL AUTO_INCREMENT, 
	country_code VARCHAR(2) NOT NULL, 
	benchmark_type VARCHAR(150) NOT NULL, 
	context TEXT NOT NULL, 
	amount NUMERIC(20, 4), 
	currency_code VARCHAR(3), 
	unit VARCHAR(100), 
	period VARCHAR(100), 
	geography VARCHAR(150), 
	reference_date VARCHAR(100), 
	source_id INTEGER, 
	verification_status VARCHAR(100) NOT NULL, 
	notes TEXT, 
	PRIMARY KEY (benchmark_id), 
	FOREIGN KEY(country_code) REFERENCES countries (country_code), 
	FOREIGN KEY(source_id) REFERENCES sources (source_id)
)ENGINE=InnoDB

;


CREATE TABLE IF NOT EXISTS fx_rates (
	fx_id INTEGER NOT NULL AUTO_INCREMENT, 
	base_currency VARCHAR(3) NOT NULL, 
	quote_currency VARCHAR(3) NOT NULL, 
	rate NUMERIC(24, 10), 
	rate_date VARCHAR(20), 
	rate_type VARCHAR(255), 
	source_id INTEGER, 
	verification_status VARCHAR(100) NOT NULL, 
	notes TEXT, 
	PRIMARY KEY (fx_id), 
	FOREIGN KEY(source_id) REFERENCES sources (source_id)
)ENGINE=InnoDB

;


CREATE TABLE IF NOT EXISTS payment_quotes (
	quote_id INTEGER NOT NULL AUTO_INCREMENT, 
	origin_country_code VARCHAR(2) NOT NULL, 
	destination_country_code VARCHAR(2) NOT NULL, 
	provider_name VARCHAR(255), 
	origin_currency VARCHAR(3), 
	destination_currency VARCHAR(3), 
	send_amount NUMERIC(22, 4), 
	receive_amount NUMERIC(22, 4), 
	fee_amount NUMERIC(22, 4), 
	fee_currency VARCHAR(3), 
	quoted_fx_rate NUMERIC(24, 10), 
	delivery_time VARCHAR(100), 
	quote_timestamp VARCHAR(40), 
	quote_expiry VARCHAR(40), 
	source_url TEXT, 
	verification_status VARCHAR(100) NOT NULL, 
	notes TEXT, 
	PRIMARY KEY (quote_id), 
	FOREIGN KEY(origin_country_code) REFERENCES countries (country_code), 
	FOREIGN KEY(destination_country_code) REFERENCES countries (country_code)
)ENGINE=InnoDB

;


CREATE TABLE IF NOT EXISTS transactions (
	id VARCHAR(45) NOT NULL, 
	plan_id VARCHAR(40) NOT NULL, 
	quote_id VARCHAR(80) NOT NULL, 
	created_at VARCHAR(40) NOT NULL, 
	status VARCHAR(40) NOT NULL, 
	approved_amount NUMERIC(22, 4) NOT NULL, 
	currency VARCHAR(3) NOT NULL, 
	simulation_only INTEGER NOT NULL, 
	idempotency_key VARCHAR(120) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(plan_id) REFERENCES plans (id), 
	UNIQUE (idempotency_key)
)ENGINE=InnoDB

;


CREATE TABLE IF NOT EXISTS tuition_benchmarks (
	tuition_id INTEGER NOT NULL AUTO_INCREMENT, 
	country_code VARCHAR(2) NOT NULL, 
	institution VARCHAR(255), 
	program VARCHAR(500) NOT NULL, 
	level VARCHAR(100), 
	student_type VARCHAR(150), 
	amount NUMERIC(20, 4), 
	currency_code VARCHAR(3), 
	fee_basis VARCHAR(100), 
	academic_year VARCHAR(100), 
	source_id INTEGER, 
	verification_status VARCHAR(100) NOT NULL, 
	notes TEXT, 
	PRIMARY KEY (tuition_id), 
	FOREIGN KEY(country_code) REFERENCES countries (country_code), 
	FOREIGN KEY(source_id) REFERENCES sources (source_id)
)ENGINE=InnoDB

;

INSERT IGNORE INTO audit_chain_state(state_id,last_hash) VALUES (1,'GENESIS');
