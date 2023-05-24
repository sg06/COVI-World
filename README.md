# COVI-World: NEWS and Statistics Handout

In this project, we have developed a comprehensive solution called COVI-World. This terminal-based portal provides a centralized hub for accessing COVID-19 statistics and news from various countries, continents, and worldwide. The implementation involved the utilization of PLY or Lex/Yacc in establishing grammar rules for extracting query results, handling potential errors, and logging the results in a dedicated file.
<br><br>
To gather COVID-19 statistics, we crawled the Worldometer website and saved the pages corresponding to the countries listed in the "worldometers_countrylist.txt" in HTML format. Subsequently, we devised grammar rules using PLY or Lex/Yacc tools to extract specific fields such as total cases, active cases, total deaths, total recovered, total tests, and more for any desired country, continent, or global data.
<br><br>
The extraction process also encompassed additional information, such as the percentage of total world cases for each field, utilizing data from the previous day. Furthermore, we address user queries of a particular country, continent, world and time range. Examples of such queries include changes in active cases, daily death toll, new recovered cases, and new cases, as well as finding the most similar country to a given query.
<br><br>
Similarly, we crawled the Wikipedia page dedicated to the COVID-19 timeline to collect news updates for all the countries listed in the "covid_country_list.txt" file. We processed user queries related to specific time ranges using the extracted news data. The queries can include
- Showcasing global news and responses within the specified time range,
- Generating word clouds to visualize the extracted information,
- Comparing word clouds for different time ranges,
- Determining the available date range for news information of a specific country,
- Extracting news and generating word clouds for a country and specified date range, and
- Identifying the top three closest countries based on Jaccard similarity of the extracted information and COVID-related terms.
<br>
We have developed a user-friendly menu-driven program that provides a lightweight interface to facilitate easy access to all COVID-related queries. This program allows users to navigate various options and retrieve the desired COVID-19 information seamlessly.
