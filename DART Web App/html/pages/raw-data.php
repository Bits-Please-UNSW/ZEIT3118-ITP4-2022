<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="../style.css">
        <script src="../main.js"></script>
    </head>
    <body>
        <nav>
            <div class="logo">
                <a class="logo-link" href="../index.php"><img class="logo-img"></a>
            </div>
            <div class="heading">
                <h1 class="site-title">DART: Data Anomaly Recognition Tool</h1>
            </div>
            <div class="nav">
                <a href="raw-data.php" class="nav-buttons">Raw Data</a>
                <a href="data.php" class="nav-buttons">Data Plots</a>
                <a href="anomaly.php" class="nav-buttons">Logged Anomalies</a>
            </div>
        </nav>
        <!--Site Content-->
        <div class="container">
            <h2>Raw data lookup</h2>
            
            
            <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
                <label for="start-date">Search Start:</label>
                <input type="date" id="start-date" name="start-date">
                <input type="time" id="start-time" name="start-time" value="00:00:00">
                <br>
                <label for="end-date">Search End:</label>
                <input type="date" id="end-date" name="end-date">
                <input type="time" id="end-time" name="end-time" value="12:00:00">
                <br>
                <input type="submit" value="Search">
            </form>

            <?php
                $conn = mysqli_connect('localhost', 'dartuser', 'password1', 'dart_data');
                if (!$conn) {
                    echo "Crashed";
                }
                $sql="SELECT * FROM sensor_data";
                $out=$conn->query($sql);
                echo "There are <u>" . $out->num_rows . "</u> datapoints in the database.<br>";

                // Collect values from post
                $start_date = $_POST["start-date"];
                $start_date = date("Y-m-d", strtotime($start_date));
                $start_time = $_POST["start-time"];

                $end_date = $_POST["end-date"];
                $end_time = $_POST["end-time"];

                $start = "$start_date $start_time";
                $end = "$end_date $end_time";

                if($start!=0 && $end != 0) {
                    echo "Your search starts at <u>$start</u>, and ends at <u>$end</u>, yielding <u>";
                    $sql = "SELECT * FROM sensor_data WHERE (DATETIMESTAMP>='$start' AND DATETIMESTAMP<='$end')";
                    $out=$conn->query($sql);
                    $num_results = $out->num_rows;
                    echo $num_results . "</u> results.<br>";
                    $results = array();
                    while($row = mysqli_fetch_array($out)) {
                        $results[] = $row;
                    }
                    if ($num_results != 0) {
                        echo "<div class='raw-data-table-container'><table class='raw-data-table'><tr><th>Timestamp</th><th>Temperature (&#176;C)</th><th>Humidity (%)</th></tr>";
                        foreach($results as $point) {
                            $count=1;
                            echo "<tr>";
                            foreach($point as $value) {
                                if($count) {
                                    echo "<td>" . $value . "</td>";
                                }
                                $count = !$count;
                            }
                            echo "</tr>";
                        }
                        echo "</table></div><br> End of Results.";
                    }
                }
                $conn->close();
            ?>
            
        </div>
        <div class="sidebar"><!-- displays anomalies from the last round of training -->
            <h2>Recent Anomalies:</h2>
            <p> Anomalies detected in the last round of training for the Machine Learning model</p>
            <?php 
                $path = "../data/RecentAnomalies.csv";
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
</html>