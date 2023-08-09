# This script will process an input file of MAC addresses and output a file containing the vendor for each MAC
# requires mac-vendor-lookup library installed with pip install mac-vendor-lookup
# v3 updates
# - add some error handling
# - perform mac database update during runtime

from mac_vendor_lookup import MacLookup, BaseMacLookup
import csv

# instantiate an object of type MacLookup
mac = MacLookup()

# define input and output files
macFile = "mac.csv"
macVendorFile = "macs with vendors.csv"

# list of mac-vendor dictionaries to store key:value pairs of lookup values
macVendor = []
macVendor_columns = ["MacAddress", "MacVendor"]

# test a lookup call
#print(mac.lookup("6c2b.59cb.7d5e"))

# default method of pulling the latest mac vendor database
# this didn't work for me as the database file wasn't where it was expected to be
#mac.update_vendors()

# alternate method of updating the mac vendor file if it is stored
# in a custom or nonstandard location
# find the local vendor file if it is non-standard and set the cache_path
macVendorText = mac.find_vendors_list()
#print(f"vendor list location is {macVendorText}")
print("Updating MAC Vendors File mac-vendors.txt. Please Wait")
BaseMacLookup.cache_path = macVendorText
mac.update_vendors()


# try a mac lookup.  if success vendor equals the returned vendor value.
# if the lookup throws and exception error assign vendor the value UNKNOWN
# append the MAC and the final vendor value to the list of mac-vendor dictionaries
with open(macFile, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        try:
            vendor = mac.lookup(row[0])
        except KeyError as e:
            vendor = "UNKNOWN"
        macVendor.append({"MacAddress": row[0],
                                "MacVendor": vendor})

# output the list of mac-vendor dictionaries to a csv file
with open(macVendorFile, "w") as file:
    writer = csv.DictWriter(file, fieldnames=macVendor_columns)
    for item in macVendor:
        writer.writerow(item)
