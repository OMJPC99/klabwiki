type file;

app (file big_files, file small_files) retrieve_files (file retriever) {
    retrieve_files @retriever @big_files @small_files;
}

app (file out, file err) transfer_and_split (file transfer_script, file split_script, string file_name, int file_count) {
    transfer_and_split @transfer_script @split_script file_name file_count stdout=filename(out) stderr=filename(err);
}

file retriever <single_file_mapper; file="retrieve_bucket_list.py">;

file big_file_names <single_file_mapper; file="big_files.txt">;
file small_file_names <single_file_mapper; file="small_files.txt">;

(big_file_names, small_file_names) = retrieve_files(retriever);

string big_files[] = readData(big_file_names);
string small_files[] = readData(small_file_names);

foreach i in [0:length(big_files)-1] {
    file out <single_file_mapper; file=strcat("stdoutput/big_out_",i,".out")>;
    file err <single_file_mapper; file=strcat("stdoutput/big_err_",i,".err")>;
    file transferer <single_file_mapper; file="transfer7z.py">;
    file splitter <single_file_mapper; file="splitter.py">;
    (out, err) = transfer_and_split(transferer, splitter, big_files[i], i);
}

foreach i in [0:length(small_files)-1] {
    file out <single_file_mapper; file=strcat("stdoutput/small_out_",i,".out")>;
    file err <single_file_mapper; file=strcat("stdoutput/small_err_",i,".err")>;
    file transferer <single_file_mapper; file="transfer7z.py">;
    file splitter <single_file_mapper; file="splitter.py">;
    (out, err) = transfer_and_split(transferer, splitter, small_files[i], i);
}
