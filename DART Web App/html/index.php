<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="style.css">
        <script src="main.js"></script>
    </head>
        <nav>
            <div class="logo">
                <a class="logo-link" href="index.php"><img class="logo-img"></a>
            </div>
            <div class="heading">
                <h1 class="site-title">DART: Data Anomaly Recognition Tool</h1>
            </div>
            <div class="nav">
                <a href="./pages/raw-data.php" class="nav-buttons">Raw Data</a>
                <a href="./pages/data.php" class="nav-buttons">Data Plots</a>
                <a href="./pages/anomaly.php" class="nav-buttons">Logged Anomalies</a>
            </div>
        </nav>
    <body onload="Javascript:AutoRefresh(150000)"><!-- Auto-Refresh the page after 2.5 minutes-->
        <div class="container">
            <p class="description">Welcome to DART, also known as the Data Anomaly Recognition Tool, developed by 'Bits, Please.'
                <br><br>
                This application employs a One-Class Support Vector Machine - machine learning algorithm model to intelligently detect, 
                graph and display anomalous temperature and humidity data collected by a DHT11 sensor. 
                Designed for use with smart industrial controllers, DART reads this logged environment telemetry from an SQL database every 30 minutes, 
                compares the values to the aggregate data recorded over the last 24 hours, and displays any potentially anomalous values detected for the user to investigate, 
                in near real-time. This data is then displayed in both raw-text format, as well as in a colour-coded scatter plot showing the relationship between each of the readings 
                versus the decision function used to determine if the data is anomalous or not.
                <br><br>
                To get started, navigate to the 'Raw Data', 'Data Plots' or 'Logged Anomalies' page using the navigation bar.
            </p>
            <br>
            <img src="images/Crow-pi.jpg" style="position: relative; height: 1000px;">
        </div>
        <div class="sidebar"><!-- displays anomalies from the last round of training -->
            <h2>Recent Anomalies:</h2>
            <p> Anomalies detected in the last round of training for the Machine Learning model</p>
            <?php 
                $path = "./data/RecentAnomalies.csv";
                if(0 == filesize( $path)){
                    echo "No recent anomalies";
                }else{
                    $anomalies = fopen($path,"r");
                    while (! feof($anomalies)) {
                        echo fgets($anomalies) . "<br>";
                    }
                    fclose($anomalies);
                }
            ?>
        </div>
    </body>
</html>
