
var map, osm_layer, vector_layer, point_layer;
var epsg_4326, epsg_900913;
var proj_opts;
var features_data;
var features = [];
var selected_f;
var url;
var s_style, t_style, m_style;
var selectctrl, selectpointctrl;
var tid;
var tids;
var tid_i = -1;
      
function init(){
	epsg_4326 = new OpenLayers.Projection("EPSG:4326");
	epsg_900913 = new OpenLayers.Projection("EPSG:900913");
	proj_opts = {
		'internalProjection': epsg_900913,
		'externalProjection': epsg_4326
	};

	map = new OpenLayers.Map('map');

	osm_layer = new OpenLayers.Layer.OSM("OpenLayers OSM");
	var defaultstyle = new OpenLayers.Style({strokeColor:"#000000", strokeWidth:2, strokeOpacity:1});
	var tempstyle = new OpenLayers.Style({strokeColor:"#ff0000", strokeWidth:3, strokOpacity:1.0});
	var selectstyle = new OpenLayers.Style({strokeColor:"#0000ff", strokeWidth:3, strokOpacity:1.0});
	vector_layer = new OpenLayers.Layer.Vector("routelayer", {styleMap: new OpenLayers.StyleMap({'default':defaultstyle, 'temporary':tempstyle, 'select':selectstyle})});
	point_layer = new OpenLayers.Layer.Vector("pointlayer");
	
	map.addLayers([osm_layer, vector_layer, point_layer]);


	var highlightctrl = new OpenLayers.Control.SelectFeature(vector_layer, {hover:true, highlightOnly:true, renderIntent:"temporary"});
	map.addControl(highlightctrl);
	highlightctrl.activate();

	map.addControl(new OpenLayers.Control.MousePosition({displayProjection:epsg_4326}));

	map.setCenter(new OpenLayers.LonLat(12953390, 4848000), 11);

	t_style = {
                strokeColor: "#00FF00",
				strokOpacity: 1,
				fillColor: "#00ff00",
				fillOpacity: 0.5,
                pointRadius: 5,
            };

	s_style = {
                strokeColor: "#FF0000",
				strokOpacity: 1,
				fillColor: "#FF0000",
				fillOpacity: 0.5,
                pointRadius: 5,
            };
	m_style = {
                strokeColor: "#0000ff",
				strokOpacity: 1,
				fillColor: "#0000ff",
				fillOpacity: 0.3,
                pointRadius: 5,
            };
}

function get_tids(fromtid, totid) {
	url = "../php/get_tids.php";
	tid_i = -1;
	$.ajax({
		url: url,
		data: {fromtid:fromtid, totid:totid},
  		success: get_tids_done,
		error: info_error
	});
}

function get_tids_done(data) {
	if (data == ':(') {
		set_tid_info(':(');
	}else {
		tids = $.parseJSON(data);
		if (tids.length > 0) {
			set_tid_info(tids.length + ' Left. COME ON !!');
		} else {
			set_tid_info('All DONE :D');
		}
	}
}

function get_track_data(filename) {
	if (filename) {
		url = "../data/tracks/" + filename;
		if(!url.match(/json$/)){
			str = url + ".json";		
		}
		$.ajax({
			url: url,
  			success: get_track_done,
			error: info_error
		});
	}
}

function get_path_data(filename) {
	if (filename) {
		url = "../data/paths/" + filename;
		if(!url.match(/json$/)){
			str = url + ".json";		
		}
		$.ajax({
			url: url,
  			success: get_path_done,
			error: info_error
		});
	}
}

function get_next_data() {
	set_info(':|');
	tid_i = tid_i + 1;
	if(tid_i >= tids.length) {
		set_tid_info('All DONE :D');
		return;
	}
	tid = tids[tid_i]['tid'];
	set_tid_info(tid);
	track_filename = "geojson_t_" + tid;
	get_track_data(track_filename);
}

function get_track_done(jsondata) {
	//plot_track(jsondata, false);
	plot_gps(jsondata);
	path_filename = "geojson_p_BN_" + tid;
	get_path_data(path_filename);
}

function get_path_done(jsondata) {
	plot_track(jsondata);
}

function insert_data(valid) {
	url = "../php/insert_path.php"
	$.ajax({
		url: url,
		data: {tid:tid, valid:valid},
  		success: set_info,
		error: info_error
	});
}

function plot_track(jsondata) {	
	features = [];
	vector_layer.removeAllFeatures();
	var geojsoner = new OpenLayers.Format.GeoJSON(proj_opts);
	var tmp_fs = geojsoner.read(jsondata);
	if(tmp_fs) {
		if(tmp_fs.constructor != Array) {
			tmp_fs = [tmp_fs];
		}
		features = features.concat(tmp_fs);
        vector_layer.addFeatures(features);		
	}else{
		alert(url + " is broken");
	}
}

function replot_track() {
	vector_layer.removeAllFeatures();
	point_layer.removeAllFeatures();
	selectctrl.activate();
	vector_layer.addFeatures(features);
	selectctrl.unselect(selected_f);
}

function plot_gps(jsondata) {
	point_layer.removeAllFeatures();
	var geojsoner = new OpenLayers.Format.GeoJSON(proj_opts);
	var feature = geojsoner.read(jsondata);
	if(feature) {
		if(feature.constructor == Array) {
			feature = feature[0];
		}
		var lonlats = feature.geometry.clone().transform(epsg_900913, epsg_4326).getVertices();
		var lonlats2 = feature.geometry.getVertices();

		var pnum = lonlats2.length;
		var points = [];

		for(var i=1; i < pnum-1; i++){
			points.push(new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Point(lonlats2[i].x, lonlats2[i].y), null, m_style));	
		}
		points.push(new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Point(lonlats2[0].x, lonlats2[0].y), null, s_style));	
		points.push(new OpenLayers.Feature.Vector(new OpenLayers.Geometry.Point(lonlats2[pnum-1].x, lonlats2[pnum-1].y), null, t_style));	
		point_layer.addFeatures(points);
	}else{
		alert(url + " is broken");
	}
}

function clear() {
}

function info_error(e) {
	alert(e);
}

