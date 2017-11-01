SET pg_bin=C:\Program Files\PostgreSQL\9.6\bin\
SET exec=psql.exe
SET PGPASSWORD=ebaeba18

echo %time% >> result.txt

"%pg_bin%%exec%" -U eba -d eba -c "SELECT min(fid), max(fid), count(fid) FROM amazon_palsar;" >> result.txt
"%pg_bin%%exec%" -U eba -d eba -c "SELECT last_value FROM amazon_palsar_seq;" >> result.txt
"%pg_bin%%exec%" -U eba -d eba -c "SELECT count(processed) as count_processed FROM amazon_palsar WHERE processed = FALSE;" >> result.txt

"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_max from amazon_palsar where trmm_max is not null;" >> result.txt
"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_mean from amazon_palsar where trmm_mean is not null;" >> result.txt
"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_median from amazon_palsar where trmm_median is not null;" >> result.txt
"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_min from amazon_palsar where trmm_min is not null;" >> result.txt
"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_q1 from amazon_palsar where trmm_q1 is not null;" >> result.txt
"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_q3 from amazon_palsar where trmm_q3 is not null;" >> result.txt
"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_sd from amazon_palsar where trmm_sd is not null;" >> result.txt
"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_soil from amazon_palsar where f_soil_qr is not null;" >> result.txt
"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_vegetation from amazon_palsar where vegetation is not null;" >> result.txt

"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_palsar_hh from amazon_palsar where palsar_hh is not null;" >> result.txt
"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as palsar_hhrhv1 from amazon_palsar where palsar_hhrhv1 is not null;" >> result.txt
"%pg_bin%%exec%" -U eba -d eba -c "select count(*) as count_palsar_hv from amazon_palsar where palsar_hv is not null;" >> result.txt

