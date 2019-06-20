# desensitize_excel
Anonymize data in excel sheet by hashing or masking selected columns. 

### Install Python Packages ###
```
pip3 install --user -r requirements.txt
```

### Run ###
```
python3 desensitizer.py sample.xlsx Sheet1 id,name contact,email
```

### Use existing character map dictionary ###
```
python3 desensitizer.py sample.xlsx Sheet1 id,name contact,email sample_char_map.csv
```
Using same character map dictionary will produce same masked output for same sting values.

### Output Generated ###
Two CSV files will be written out to the current directory.

CSV File Name | Content
-- | --
excel.sheet.csv | Anonymized data in pipe delimited CSV format.
excel.sheet.char_map.csv | Character map set used to mask alphanumeric characters.
