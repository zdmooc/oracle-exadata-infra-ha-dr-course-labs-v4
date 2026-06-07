set pages 200 lines 220
prompt READ ONLY ASM healthcheck
select name,type,total_mb,free_mb,usable_file_mb,state from v$asm_diskgroup;
select name,path,failgroup,mount_status,mode_status,state from v$asm_disk order by group_number,name;
