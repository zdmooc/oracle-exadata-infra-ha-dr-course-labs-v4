set pages 200 lines 220
prompt READ ONLY AWR/ASH examples - adapter licence Diagnostics Pack
select event,count(*) samples from v$active_session_history where sample_time > systimestamp - interval 15 minute group by event order by samples desc;
select sql_id,elapsed_time,executions,disk_reads,buffer_gets from v$sql order by elapsed_time desc fetch first 20 rows only;
