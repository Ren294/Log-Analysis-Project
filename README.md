# Big Data Project: NASA Log Analytics Process

## Project Objective

The primary goal of this project is to develop a scalable and fault-tolerant log analytics pipeline based on the Lambda architecture. The system ingests, processes, and analyzes NASA server logs in both real-time and batch modes. This enables immediate insights for real-time monitoring and generates comprehensive reports for periodic analysis.

## Datasets Selection
NASA access log dataset 1995:
- <a href = https://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html> Actual NASA Logs </a>
- <a href = https://www.kaggle.com/souhagaa/nasa-access-log-dataset-1995/download> Kaggle </a>

This dataset is particularly valuable for several reasons. First, it captures a high volume of real-world web traffic, providing a realistic basis for our analysis. Secon d, the data spans different times of the day and days of the week, enabling us to id entify patterns and trends in server usage. Lastly, the inclusion of various HTTP res ponse codes and byte sizes allows us to assess not only the traffic but also the ser ver's performance and potential issues such as error rates and load.
## System Architecture
The system is divided into several layers, each responsible for specific tasks within the log analytics process:

### Ingestion Layer
- **Apache NiFi**: Efficiently ingests NASA logs from various sources, enabling flexible and scalable data flow management.

### Speed Layer
- **Apache Kafka**: Serves as a high-throughput, low-latency message broker, handling real-time data streams.
- **Apache Spark Streaming**: Processes data streams in real-time, enabling immediate analytics and rapid response to events. Integrates seamlessly with Kafka for continuous log processing.

### Batch Layer
- **Hadoop HDFS**: Acts as the primary storage for large volumes of log data, ensuring high availability and scalability.
- **Apache Spark**: Performs batch processing on data stored in HDFS, facilitating complex data analysis tasks.
- **Apache Hive**: Provides a data warehouse infrastructure, enabling efficient querying and analysis of large datasets stored in HDFS.

### Serving Layer
- **Apache Cassandra**: Stores processed data with fast read/write capabilities, particularly useful for real-time analytics.

### Analytics Layer
- **Grafana**: Offers real-time visualization of log data through dynamic dashboards and alerts.
- **Power BI**: Generates detailed daily, monthly, and periodic reports, providing deep insights through comprehensive visualizations.

## Technologies Used

- **Operating System**: Ubuntu Server 24.04 LTS
- **Programming Languages**: Python
- **Libraries and Frameworks**: 
  - Apache NiFi
  - Apache Kafka
  - Apache Spark 
  - Hadoop HDFS
  - Apache Hive
  - Apache Cassandra
  - Grafana
  - Power BI
- **Database**: Cassandra for real-time data storage and Hive for batch queries

## Installation and Deployment

### System Requirements
- Java 8+
- Python 3.7+
- Apache Hadoop
- Apache Kafka
- Apache Spark
- Apache Hive
- Apache NiFi
- Grafana
- Power BI

### Installation
- Follow the official documentation to install the required components on Ubuntu Server.

### Running the Project
1. Start Apache NiFi to begin ingesting NASA log data.
2. Run Kafka and Spark Streaming jobs for real-time processing.
3. Use Spark and Hive for batch processing and querying historical data.
4. Set up Grafana dashboards for real-time monitoring.
5. Generate periodic reports using Power BI.

### Configuration
- Configure NiFi to route logs to Kafka.
- Set up Kafka topics and configure Spark Streaming to consume from these topics.
- Adjust Hive configurations for efficient querying.
- Integrate Grafana with Cassandra for real-time visualization.

## Usage

- **Input Data**: NASA server logs, including access logs, error logs, and application logs.
- **Running Data Processing Jobs**:
  - Real-time processing: Kafka + Spark Streaming jobs
  - Batch processing: Spark jobs on data stored in HDFS
- **Output Data**:
  - Real-time metrics displayed on Grafana dashboards.
  - Aggregated and historical reports available in Power BI.

## Results and Analysis

- **Real-time Monitoring**: Provides immediate insights through Grafana dashboards with critical event alerts.
- **Batch Analysis**: Enables deep dives into historical data using complex queries via Hive, with results visualized in Power BI.

## Notes and Considerations

- Ensure optimal Kafka and Spark configurations for performance.
- Regularly monitor HDFS storage capacity to prevent data overflow.
- Customize Grafana dashboards to meet specific monitoring needs.

## References

- [Apache NiFi Documentation](https://nifi.apache.org/docs.html)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Hadoop Documentation](https://hadoop.apache.org/docs/stable/)
- [Hive Documentation](https://cwiki.apache.org/confluence/display/Hive/Home)
- [Cassandra Documentation](https://cassandra.apache.org/doc/latest/)

## Contribution

To contribute, fork the repository, make your changes, and submit a pull request. Issues and suggestions for improvement are welcome.
