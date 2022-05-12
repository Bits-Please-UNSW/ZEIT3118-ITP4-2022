<!DOCTYPE html>
<html>
    
    <head>
        <link rel="stylesheet" href="style.css">
        <script src="main.js"></script>
    </head>
        <nav>
            <div class="logo">
                <img class="logo-img">
            </div>
            <div class="heading">
                <h1 class="site-title">DART: Data Anomaly Recognition Tool</h4>
            </div>
            <div class="nav">
                <a href="./pages/data.php" class="nav-buttons">Data Plots</a>
                <a href="./pages/anomaly.php" class="nav-buttons">Logged Anomalies</a>
                <a href="./pages/login.php" class="nav-buttons">Log Out</a>
            </div>
        </nav>
    <body onload="Javascript:AutoRefresh(15000)"><!-- Auto-Refresh the page after 2.5 minutes--><!-- Set back to 150000 after presentation -->
        <div class="container">
            <p>Dart, or the Data Anomaly Recognition Tool developed by Bits Please, employs a One-Class SVM Machine Learning model 
                to intelligently recognise and flag anomalous data in a data set. Designed for use with smart industrial controllers,
                Dart reads data from a comma separated values (csv) file every 30 minutes, and compares it to the trends of the last 24
                hours, flagging any potentially-anomalous values. It then displays the data and anomalies neatly for the user, with a
                colour-coded scatter plot showing the ______ of each of the readings.<br>
                <br>
                To get started, navigate to the data or anomalies page in the navigation bar.
            </p>
            <?php echo 'Oh hi there' ?>
        </div>
        <div class="sidebar">
            <p>This is a sidebar</p>
        </div>
    </body>
</html>
