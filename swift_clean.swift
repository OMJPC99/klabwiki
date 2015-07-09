type file;

# interval_size is the number of files per subset to be passed to workers
# file_list is the list of split files in the bucket
# file_interval_count is the number of distinct intervals fit into the file_list
app (file file_list) get_files (file lister) {
    get_files @lister @file_list;
}

# scraper - clean_and_ingest.py
# 	cleaner - grep_cleaner.py
#	ingester - UniversalIngest.py
#	filterer - filter_database.py
app (file ip_list, file out, file err) final_data_scrape (file scraper, file_cleaner, file ingester, file filterer) {
    final_data_scrape @scraper @ip_list stdout=filename(out) stderr=filename(err);
}

file lister <single_file_mapper; file="get_split_list.py">;
file file_list <single_file_mapper; file="split_file_list.txt">;

file_list = get_files(lister);
string split_files[] = readData(file_list);

file scraper <single_file_mapper; file="clean_and_ingest.py">;
file cleaner <single_file_mapper; file="grep_cleaner.py">;
file ingester <single_file_mapper; file="UniversalIngest.py">;
file filterer <single_file_mapper; file="filter_database.py">;

foreach split_file,i in split_files {
    file out <single_file_mapper; file=strcat("stdout/stdout_",i,".out")>;
    file err <single_file_mapper; file=strcat("stdout/stderr_",i,".err")>;
    file final_output <single_file_mapper; file=strcat("output/ip_list_",i,".txt")>;
    (final_output, out, err) = final_data_scrape(scraper, cleaner, ingester, filterer);
}