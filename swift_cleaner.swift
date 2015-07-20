type file;

# script - the python script to transfer a group of files, clean, ingest, and filter
# group - the name of the group of split files to be used
# dbname - the name of the mysql database to be used (this ensures that an individual worker has no conflicts)
# filtered_output - a text file with the rows of the db that contain a cite_journal tag
# out - the stdout of the script
# err - the stderr of the script
app (file filtered_output, file out, file err) analyze (file main_script, file group_transferer, file cleaner, file ingester, file filterer, file ip_lookup, string group, string dbname) {
    analyze @main_script group dbname @filtered_output stderr=@err stdout=@out;
}

# retrieve - script that lists the groups in the AWS S3 bucket
# group_list - a text file that contains a list of the groups
# out - the stdout of the script
# err - the stderr of the script
app (file group_list, file out, file err) get_bucket_groups (file retrieve) {
    get_bucket_groups @retrieve @group_list stderr=@err stdout=@out;
}

app (file final_output) concatenate (file f_outs[]) {
    concatenate @filenames(f_outs) ">" @final_output;
}

file analyzer <single_file_mapper; file="transfer_clean_ingest_filter.py">;
file transferer <single_file_mapper; file="transfer_by_group.py">;
file cleaner <single_file_mapper; file="grep_cleaner.py">;
file ingester <single_file_mapper; file="UniversalIngest.py">;
file filterer <single_file_mapper; file="filter_database.py">;
file lookuper <single_file_mapper; file="ip_lookup.py">;
file retriever <single_file_mapper; file="sort_bucket_by_group.py">;

file list <single_file_mapper; file="group_list.txt">;
file std_out <single_file_mapper; file="stdoutput/bucket_retrieval.out">;
file std_err <single_file_mapper; file="stdoutput/bucket_retrieval.err">;
(list, std_out, std_err) = get_bucket_groups(retriever);

string group_names[] = readData(list);

file f_outputs[];

foreach i in [0:length(group_names)-1] {
    file out <single_file_mapper; file=strcat("stdoutput/wiki_stdout_",i,".out")>;
    file err <single_file_mapper; file=strcat("stdoutput/wiki_stderr_",i,".err")>;
    file filtered_output <single_file_mapper; file=strcat("output/wiki_output_", i, ".txt")>;
    (filtered_output, out, err) = analyze(analyzer, transferer, cleaner, ingester, filterer, lookuper, group_names[i], strcat("wikibase_",i));
    f_outputs[i] = filtered_output;
}

file final_output <single_file_mapper; file="final_wiki_output.txt">;
final_output = concatenate(f_outputs);
