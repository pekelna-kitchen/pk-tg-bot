ALTER TABLE "public"."hkdb_products" ADD symbol varchar(1);
-- ALTER TABLE "public"."hkdb_products" ALTER COLUMN symbol TEXT CHARSET utf8mb4;
ALTER TABLE "public"."hkdb_products" ADD limit_container_id int;
ALTER TABLE "public"."hkdb_products" ADD FOREIGN KEY(limit_container_id)  REFERENCES "public"."hkdb_containers"(id);
DROP TABLE "public"."hkdb_limits";
