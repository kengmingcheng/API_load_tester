# API load testing tool

For most configuration of this testing app, you could find it in the ./resources/config.properties

To start this tester, just navigate to where the tester is and type following command in terminal:
```
python3 main.py
```

## Explanation in config.properties
---
### server
* target server of the test
### api
* target api of the test
### content-type
* acceptable options: xml, json
### source
* the source file that contend account information
### loop
* number of loop per thread the entire test will execute
### thread
* number of thread per source the entire test will execute
### interval
* the interval between each request for a thread
### 1to1_Or_1toM_flag
* define the location of flag for "1to1" or "1toM"

### payload

By appending ".<payload_field> = <payload_value>", you can add extra payloads to the default payload file. For instance:
```
payload.my_test_field = my_test_value
payload.my_another_field = my_another_value
```
This will append new fields to the payload, like:
```
{
    "my_test_field": "my_test_value",
    "my_another_field": "my_another_value"
}
```

### headers

Similar to paylaod, you can also customize content in the headers using "headers.<headers_field> = <headers_value>". For example:
```
headers.my_test_header = my_header_value
headers.my_another_headers = my_another_header_value
```
This will append new fields to the headers, like:
```
Request Headers
    my_test_header: my_header_value
    my_another_headers: my_another_header_value
```
