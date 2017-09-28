import pandas as pd

# import the CSV from http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html
# this will return a pandas dataframe.
kddcup = r'E:\heitor.guerra\PycharmProjects\pyLiDARForest\app\sklearn\kddcup.data_10_percent.csv'
col_names = ["duration", "protocol_type", "service", "flag", "src_bytes",
             "dst_bytes", "land", "wrong_fragment", "urgent", "hot", "num_failed_logins",
             "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root",
             "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
             "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
             "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
             "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
             "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
             "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
             "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label"]

print(len(col_names))
data = pd.read_csv(kddcup, header=None, names=col_names, low_memory=False)

# extract just the logged-in HTTP accesses from the data
# data = data[data['service'] == "http"]
# data = data[data["logged_in"] == 1]

# # let's take a look at the types of attack labels are present in the data.
# data.label.value_counts().plot(kind='bar')