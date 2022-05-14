# earthquakes
This repository aims to create a seismological observatory consuming USGS API data using python. The idea of this project is to collect seismological earthquake data above 3.5 degrees on the Richter scale from the period from 01/01/1970 to 2022. All the technical explanation about the process of creating this solution is on the PDF file that is in Portuguese.

<p align="center">
  <img src="https://www.google.com/url?sa=i&url=https%3A%2F%2Flegacy.etap.org%2Fdemo%2FEarth_Science%2Fes3%2Finstruction5tutor.html&psig=AOvVaw3PPe4X29h_zDNbQgF8GFmD&ust=1652573330865000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCKCf58bZ3fcCFQAAAAAdAAAAABAJ" />
</p>

The suggested architecture for this solution is simple, as shown on the PDF file. Using python to manipulate the data on ETL (and schedule it with Watson Studio) and insert it into PostgreSQL to make an interactive view with streamlit library.


