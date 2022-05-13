<!DOCTYPE html>
<html>
    
    <head>
        <link rel="stylesheet" href="../style.css">
        <script src="../main.js"></script>
    </head>
    <body onload="Javascript:AutoRefresh(150000)"><!-- Auto-Refresh the page after 2.5 minutes-->
        <nav>
            <div class="logo">
                <a class="logo-link" href="../index.php"><img class="logo-img"></a>
            </div>
            <div class="heading">
                <h1 class="site-title">DART: Data Anomaly Recognition Tool</h4>
            </div>
            <div class="nav">
                <a href="data.php" class="nav-buttons">Data Plots</a>
                <a href="anomaly.php" class="nav-buttons">Logged Anomalies</a>
            </div>
        </nav>
        <!--Site Content-->
        <div class="container">
        <h2>All Anomalies (Last 24h):</h2>
            <p> Anomalies detected in the last 48 rounds of training for the Machine Learning model</p>
            <?php 
                $path = "../data/Anomalies.csv";
                $anomalies = fopen($path,"r");
                while (! feof($anomalies)) {
                    echo fgets($anomalies) . "<br>";
                }
                fclose($anomalies);

            ?>
        </div>
        <div class="sidebar"><!-- displays anomalies from the last round of training -->
        <h2>Recent Anomalies:</h2>
            <p> Anomalies detected in the last round of training for the Machine Learning model</p>
            <?php 
                $path = "../data/RecentAnomalies.csv";
                $anomalies = fopen($path,"r");
                while (! feof($anomalies)) {
                    echo fgets($anomalies) . "<br>";
                }
                fclose($anomalies);
            ?>
        </div>
    </body>
</html>
