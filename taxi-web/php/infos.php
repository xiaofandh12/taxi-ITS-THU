<html>
	<body>
		<?php
			function listjson($path = '../data/') {
				$dir = opendir($path);
				while(($file = readdir($dir)) !== false) {
					$ext = pathinfo($file);
					$ext = strtolower($ext["extension"]);
					if($file != '.' && $file != '..' && $ext == 'json') {
						echo $file . '<br>';
					}
				}
			}
			
			echo "<br>";
			echo "<a href='http://219.223.168.200/taxi-web/html/track.html'>raw track data</a> <br>";
			echo "<a href='http://219.223.168.200/taxi-web/html/trackinfo.html'>raw track data with GPS records</a> <br>";
			echo "<a href='http://219.223.168.200/taxi-web/html/path.html'>path data</a> <br>";
			echo "<br>";
			echo "1. Track files are named '<b>geojson_t_tid</b>'<br>";
			echo "2. Path files are named '<b>geojson_p_method_tid</b>'<br>";
			echo "Where <b>tid</b> is ID of track in database, <b>method</b> is map matching method used<br>";
			echo "<b>method</b>:{BN}<br>";
			echo "<br>";
			echo "3. Input file name and click <b>Get</b> to plot them on the map<br>";
			echo "4. <b>HOLD ON</b> helps to plot all retrived tracks of paths on map<br>";
			echo "5. <b>Restore</b> replot all ploted tracks or paths<br>";
			echo "6. <b>Clear</b> clears all ploted tracks or paths<br>";
			echo "7. <b>Infos</b> links to here<br>";
			echo "<br>";	
			echo "8. In <a href='http://219.223.168.200/taxi-web/html/trackinfo.html'>raw track data with GPS records</a>, when the track  is clicked, corresponding GPS data will be displayed in the table. When the GPS point is clicked, corresponding row in the table will be highlighted <br>";

			//echo "<br>All available track files are named 'geojson_[t]_fromcuid[_tocuid]'. <br>";
			//echo "1. With 't', trajectories's destinations are limited in a certain region, without 't', destinations are unlimited. <br>";
			//echo "2. Trajectories of taxis with cuid from 'fromcuid' to 'tocuid' are included. <br>";
			//echo "<br> Other files are for tested only.<br>";

         ?>
	</body>
</html>
