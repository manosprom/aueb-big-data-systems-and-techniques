#Managed DB

## Google Cloud

SQL -> Create Instance 

## Setup connectivity do managed postgres instance
forward `managed-pg` host to the internal ip
the managed-pg is assigned to `vpc-bds` that all machines use

```bash 
gcloud compute ssh --zone=europe-west1-b bastion-1
sudo su
ssh s01

vi /etc/hosts

# append
10.9.64.3 managed-pg
```

## Create products database

Here i am connecting to the managed-postgres and i want to create the new products database to import the products.

```bash
psql -U postgres -h managed-pg -d postgres
postgres=> CREATE DATABASE products
ctrl + C
```

## Import temp_products table

Here i am using psql to run the products.sql script directly on the prodcuts database

```sql
root@s01:~# psql -U postgres -h managed-pg -d products -f products.sql 
Password for user postgres: 
SET
SET
SET
SET
SET
SET
CREATE EXTENSION
SET
SET
SET
CREATE TABLE
ALTER TABLE
COPY 2080734
REVOKE
GRANT
root@s01:~# 
```

## Verify that all items have been copied correctly
```sql
root@s01:~# psql -U postgres -h managed-pg -d products
Password for user postgres: 
psql (9.5.21, server 11.6)
WARNING: psql major version 9.5, server major version 11.
         Some psql features might not work.
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES128-GCM-SHA256, bits: 128, compression: off)
Type "help" for help.

products=> select count(*) from temp_products;
  count  
---------
 2080734
(1 row)
```