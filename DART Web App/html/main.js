function AutoRefresh( t ) {
    setTimeout("location.reload(true);", t);
 }

const archiveFolder = '/images/data_graph_archive';
const fs=require('fs');

fs.readdir(archiveFolder).forEach(file => {
    console.log(file);
});