# s3json-to-efu

Work with aws-cli:

``` pwsh
aws s3api list-objects --bucket ? | python -m s3json_to_efu --prefix s3 --output ?.efu
```

