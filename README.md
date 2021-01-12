# PPKWU-VCard-API

## API Documentation

This api will analyze panoramafirm website (from https://panoramafirm.pl/) and page, where user could generate 
a vCard for company, which they look for.
User could receive vCard (.vcf) file, compliant with the standard [RFC6350](https://tools.ietf.org/html/rfc6350) which contains detail about company. 

## Run REST server
To run this FLASK server execute in console
```
  flask run
```

## API
To use server, send your GET request to endpoint:
```
    http://localhost:8080/vcard_service
```

There are two endpoint to use:
```
get_worker_vcard
parse_and_produce_workers
```
First endpoint, parse given website and returns a vCard generated from this website.
It receive only one query param: page    
Example usage:
```
http://localhost:5000/get_worker_vcard?page=https://panoramafirm.pl/śląskie,,dąbrowa_górnicza,cieszkowskiego,4_27/fhu_nypel_uslugi_hydrauliczne_lukasz_szydlinski-sbriri_fhm.html
```

Second endpoint, parse_and_produce_workers, will scrap panoramafirm to look for companies which we are looking for.  
There are 3 query params: 
name - phrase with will be used to search  
page_count - page count to scrap, default value is 1  
limit - limitation of results, default value is 20    

Example usage:
```
http://localhost:5000/parse_and_produce_workers?name=hydraulik&limit=5&page=1
```

When limit or page_count will be invalid (not a number or below 0), service returns 400 HTML code.   
When name will be not given or it will be empty, service returns 400 HTML code.  
    
Example generated vCard from service:
```
BEGIN:VCARD
VERSION:3.0
ADR:;;ul. Zaciszna 30A;05-230 Kobyłka;mazowieckie;05-230 Kobyłka;
ADR:;;;;;;
EMAIL:joanna-kolota@wp.pl
FN:Adam Kołota Udrażnianie rur 
N:;Adam Kołota Udrażnianie rur;;;
TEL:781 266 854
URL:http://facebook.com/234873066852050
WEBSITE:http://www.udraznianierurkobylka.pl
END:VCARD
```