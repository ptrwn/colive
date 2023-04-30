DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'colive') THEN

      RAISE NOTICE 'Role "colive" already exists. Skipping.';
   ELSE
      create user colive with encrypted password '123qwe';
   END IF;
END
$do$;
CREATE DATABASE colive OWNER colive;
grant all privileges on database colive to colive;