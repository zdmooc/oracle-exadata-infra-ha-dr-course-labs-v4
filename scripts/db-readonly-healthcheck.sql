set pages 200 lines 220
prompt READ ONLY DB healthcheck
select instance_name,host_name,status from gv$instance;
select name,open_mode,database_role,log_mode,force_logging from v$database;
select con_id,name,open_mode from v$pdbs;
