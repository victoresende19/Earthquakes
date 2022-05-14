# earthquakes
This repository aims to create a seismological observatory consuming USGS API data using python. The idea of this project is to collect seismological earthquake data above 3.5 degrees on the Richter scale from the period from 01/01/1970 to 2022. All the technical explanation about the process of creating this solution is on the PDF file that is in Portuguese.

![image](https://user-images.githubusercontent.com/63743020/168402737-1f7ce7ee-b665-4702-96de-41a6323ea8f1.png)

The suggested architecture for this solution is simple, as shown below. Using python to manipulate the data on ETL (and schedule it with Watson Studio) and insert it into PostgreSQL to make an interactive view with streamlit library.

![image](https://user-images.githubusercontent.com/63743020/168402494-f646dd8e-0fbf-426a-aa88-b11fddcbcb6c.png)


