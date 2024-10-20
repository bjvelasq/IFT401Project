from datetime import timedelta
import traceback
# For exceptions
from couchbase.exceptions import CouchbaseException
# Required for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
# Required for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import ClusterOptions
from stock_user import User  # Import User class
from stock import Stock  # Import Stock Class

endpoint = "couchbases://cb.nnq3yiry4lf6y7e2.cloud.couchbase.com" # Replace this with Connection String
username = "Admin" # Replace this with  username from cluster access credentials
password = "Password123!" # Replace this with password from cluster access credentials
# User Input ends here.
# Connect options - authentication
auth = PasswordAuthenticator(username, password)
# Get a reference to our cluster
options = ClusterOptions(auth)
# Use the pre-configured profile below to avoid latency issues with your connection.
options.apply_profile("wan_development")
try:
	cluster = Cluster(endpoint, options)
	# Wait until the cluster is ready for use.
	cluster.wait_until_ready(timedelta(seconds=5))
except Exception as e:
	traceback.print_exc()
