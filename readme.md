
## API Reference

#### Get all items

```http
  GET /api/sales-data/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `platform`   | `string` | Any Platform  |
| `start_date` | `date`   | 'YYYY-DD-MM'  |
| `end_date`   | `date`   | 'YYYY-DD-MM'  |
| `category`   | `string` | Any category  |
| `state`      | `string`   | Any category  |
| `delivery_status` | `string`   |`Delivered | In Transit  |Cancelled`  |




#### Get item

```http
  GET /api/summary-metrics/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `platform`   | `string` | Any Platform  |
| `start_date` | `date`   | 'YYYY-DD-MM'  |
| `end_date`   | `date`   | 'YYYY-DD-MM'  |
| `category`   | `string` | Any category  |
| `state`      | `string`   | Any category  |
| `delivery_status` | `string`   |`Delivered | In Transit  |Cancelled`  |



#### API documentation can be found on Swagger also

Takes two numbers and returns the sum.

## Demo

[Link for demo](https://www.youtube.com/watch?v=tsDBiK9RuUs)


## How to setup project
Make sure python is installed

```bash
  create virtual env
  python virtualenv env
  pip install -r requirements.txt

  Edit .env to enter NAME,USER,PASSWORD,HOST
  
  
```


## Django Management command to load Data
I have added a custom management command to load data from csv file

```bash
  python manage.py import_data {FILE_PATH}
```





## To run server
I have added a custom management command to load data from csv file

```bash
  python manage.py runserver
  
```



once the server boots up go and these two URL's to get the UI
```bash
1. / 
2. /summary
```




