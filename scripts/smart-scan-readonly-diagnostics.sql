set pages 200 lines 220
define SQL_ID=&1
select * from table(dbms_xplan.display_cursor(&SQL_ID, null, ALLSTATS LAST +IOSTATS +PREDICATE));
select sql_id,cell_offload_eligible_bytes,cell_offload_returned_bytes,physical_read_bytes from v$sql where sql_id=&SQL_ID;
select name,value from v$sysstat where name in (cell physical IO bytes eligible for predicate offload,cell physical IO bytes saved by storage index,cell physical IO interconnect bytes returned,cell smart table scan,cell smart index scan);
