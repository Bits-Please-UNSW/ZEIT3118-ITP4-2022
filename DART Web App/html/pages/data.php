<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="../style.css">
        <script src="../main.js"></script>
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" /> 
        <meta http-equiv="Pragma" content="no-cache" /> <meta http-equiv="Expires" content="-1"/>
    </head>
    <body onload="Javascript:AutoRefresh(150000)"><!-- Auto-Refresh the page after 2.5 minutes-->
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
            <h2>Latest graph:</h2>
            <?php echo "<img src='CurrentDataGraph.png'>";?>
            <br>
            <h2>Historical graphs:</h2>
            <!-- read image names from folder and print files and links-->
            <table class='data-graphs'>
                <tr><th>Date and time of image creation</th><th>Image</th></tr>
                <?php 
                    $path = '../images/data_graph_archive/';
                    $files = array_diff(scandir($path), array('.', '..'));
                    $files = array_reverse($files);
                    foreach($files as $file){
                        echo "<tr><td><a href='$path$file'>$file</a></td><td><img src='$path$file' style='max-width:300px;'></td></tr>";
                    }
                ?>
            </table>
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