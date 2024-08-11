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
### 1. Apache Cassandra
**1.1 Run Cassandra server**
  ```
  cassandra -f
  ```
**1.2 Create a Keyspace and Table**
- Access the Cassandra Query Language (CQL) shell:
  ```
  cqlsh -u cassandra -p cassandra
  ```
- Create a keyspace:
  ```
  CREATE KEYSPACE IF NOT EXISTS loganalysis
    WITH replication = {'class':'SimpleStrategy', 'replication_factor':1};
  ```
- Create a table:
  ```
  CREATE TABLE loganalysis.nasalog (
      host text,
      time text,
      bytes text,
      extension text,
      method text,
      response text,
      time_added text,
      url text,
      PRIMARY KEY (host, time)
  ) WITH CLUSTERING ORDER BY (time ASC)
      AND additional_write_policy = '99p'
      AND bloom_filter_fp_chance = 0.01
      AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
      AND cdc = false
      AND comment = ''
      AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
      AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
      AND crc_check_chance = 1.0
      AND default_time_to_live = 0
      AND extensions = {}
      AND gc_grace_seconds = 864000
      AND max_index_interval = 2048
      AND memtable_flush_period_in_ms = 0
      AND min_index_interval = 128
      AND read_repair = 'BLOCKING'
      AND speculative_retry = '99p';
  ```
- Truncate table:
  ```
  TRUNCATE TABLE loganalysis.nasalog;
  ```
### 2. Apache Kafka
**2.1 Run Kafka server**
- Generate a new cluster ID:
  ```
  kafka-storage.sh random-uuid
  ```
- Generate the log storage:
  ```
  kafka-storage.sh format -t <uuid> -c config/kraft/server.properties
  ```
- Start Kafka Server:
  ```
  kafka-server-start.sh config/kraft/server.properties
  ```
**2.2 Create a Kafka Topic**
- Use the Kafka command-line tool to create a topic:
  ```
  kafka-topics.sh
    --create
    --bootstrap-server localhost:9092
    --topic nasa_log
    --partitions 1
    --replication-factor 1
    --if-not-exists
  ```
- List topic:
  ```
  kafka-topics.sh
    --list
    --bootstrap-server localhost:9092
  ```
- Describe topic:
  ```
  kafka-topics.sh
    --describe
    --topic nasa_log
    --bootstrap-server localhost:9092
  ```
### 3. Apache Hadoop
**3.1 Configure Hadoop**
- Follow instructions: [HadoopSingleCluster](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html)
  
**3.2 Start Hadoop services**
- Use the following commands:
  ```
  start-all.sh
  ```
- Run Example:
  ```
  hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.1.jar pi 4 100
  ```
### 4. Apache NiFi
**3.1 Run Nifi**
- Run the NiFi server:
  ```
  nifi.sh start
  ```
- Open port 8443: Ensure NiFi’s web interface is accessible at [https://localhost:8443/nifi](https://localhost:8443/nifi).

**3.2 Create workflow**
- Access NiFi’s web UI:
  ```
  https://localhost:8443/nifi
  ```
- Create a Workflow:
  
4. Use Spark and Hive for batch processing and querying historical data.
5. Set up Grafana dashboards for real-time monitoring.
6. Generate periodic reports using Power BI.

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
