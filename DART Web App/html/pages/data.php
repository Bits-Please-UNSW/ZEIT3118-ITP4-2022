<!DOCTYPE html>
<html>
    <script>

    </script>
    <head>
        <link rel="stylesheet" href="../style.css">
        <script src="../main.js"></script>
    </head>
    <body onload="Javascript:AutoRefresh(15000)"><!-- Auto-Refresh the page after 5 minutes--><!-- Set back to 150000 after presentation -->
        <nav>
            <div class="logo">
                <img class="logo-img">
            </div>
            <div class="heading">
                <h1 class="site-title">DART: Data Anomaly Recognition Tool</h4>
            </div>
            <div class="nav">
                <a href="data.php" class="nav-buttons">Data Plots</a>
                <a href="anomaly.php" class="nav-buttons">Logged Anomalies</a>
                <a href="login.php" class="nav-buttons">Log Out</a>
            </div>
        </nav>
        <!--Site Content-->
        <div class="container">
            <p>Access important information about the data <a href="https://youtu.be/dQw4w9WgXcQ">here</a>.</p><p>Logged Anomalies.<br>
                <br>
                . 
            </p>
            <img src="Test.png">
            <br>
            <!-- read image names from file and print files and links-->
            <table class='data-graphs'>
                <tr><th>Date and time of image creation</th><th>Image</th></tr>
                <?php 
                    $path = '../images/data_graph_archive/';
                    $files = scandir($path);
                    $files = array_diff(scandir($path), array('.', '..'));
                    //$files = glob($files, "*.png");
                    $files = array_reverse($files);
                    foreach($files as $file){
                        echo "<tr><td><a href='$path$file'>$file</a></td><td><img src='$path$file'></td></tr>";
                    }
                ?>
            </table>
        </div>
        <div class="sidebar">
            <p>This is a sidebar</p>
        </div>
</html>