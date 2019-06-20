# desensitize_excel
Anonymize data in excel sheet by hashing or masking selected columns. 


### Features ###

#### Hash values for selected columns
Md5 hash algorithm is used and the resulting 32 character hash string is shortened by truncating the middle portion. Example, "c4ca4238a09dje7s8a0nhs3j4js5849b" becomes "c4ca4-238a0-5849b".

#### Mask values for selected columns
A character map dictionary is generated at runtime unless provided. Alphanumeric characters [A-Za-z0-9] are encoded to a different character. Example, A --> C; B --> W; C --> X, etc. Upper and lower case letters have the same mapping. Hence, "ABC" and "abc" becomes "CWX" and "cwx" respectively.  Digits are mapped to other digits.


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
