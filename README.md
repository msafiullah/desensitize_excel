# desensitize_excel
Anonymize data in excel sheet by hashing or masking selected columns. 


## Features

#### Hash values for selected columns
Md5 hash algorithm is used and the resulting 32 character hash string is shortened by truncating the middle portion. Example, `"c4ca4238a09dje7s8a0nhs3j4js5849b"` becomes `"c4ca4-238a0-5849b"`.

#### Mask values for selected columns
A character map dictionary is generated at runtime unless provided. Alphanumeric characters [A-Za-z0-9] are encoded to a different character. Example, `A --> C; B --> W; C --> X`, etc. Upper and lower case letters have the same mapping. Hence, `"ABC"` and `"abc"` becomes `"CWX"` and `"cwx"` respectively.  Digits are mapped to other digits.

#### Sample desensitized data

***Original data***

id | name | dob | gender | contact | email
-- | -- | -- | -- | -- | --
1 | alice | 11/9/89 | F | 89389483 | alice@gmail.com
2 | ben | 23/12/93 | M | 98394853 | benjamin@outlook.com
3 | claire | 24/3/91 | F | 82938465 | clairelee@hotmail.com

***Desensitized data***


id | name | dob | gender | contact | email
-- | -- | -- | -- | -- | --
1 | 6384e-2b218-6563c | 11/9/89 | 80061-89430-71012 | 36436734 | wemgc@ltwme.gbt
2 | 7fe47-71c00-2c6aa | 23/12/93 | 69691-c7bdc-d04ac | 63467394 | icpqwtmp@bnaebbd.gbt
3 | 182e5-00f56-47bb2 | 24/3/91 | 80061-89430-71012 | 35643719 | gewmrcecc@obatwme.gbt

Columns `name` and `gender` are hashed, columns `contact` and `email` are masked, whereas columns `id` and `dob` are kept as original.


## Install Python Packages
```
pip3 install --user -r requirements.txt
```


## Run
```
python3 desensitizer.py sample.xlsx Sheet1 id,name contact,email
```

#### Use existing character map dictionary
```
python3 desensitizer.py sample.xlsx Sheet1 id,name contact,email sample_char_map.csv
```
Using same character map dictionary will produce same masked output for same sting values.


## Output Generated
Two CSV files will be written out to the current directory.

CSV File Name | Content
-- | --
excel.sheet.csv | Anonymized data in pipe delimited CSV format.
excel.sheet.char_map.csv | Character map set used to mask alphanumeric characters.
