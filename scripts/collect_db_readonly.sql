set pages 200 lines 200 trimspool on
select name, open_mode, database_role from v$database;
select inst_id, instance_name, status, host_name from gv$instance;
select name, value from v$sysstat where lower(name) like '%cell%';
select group_number, name, state, type, total_mb, free_mb from v$asm_diskgroup;
